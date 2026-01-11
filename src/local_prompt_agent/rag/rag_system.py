# -*- coding: utf-8 -*-
"""
RAG (Retrieval-Augmented Generation) system.

Simple implementation following Rule #1: Keep it simple.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from local_prompt_agent.document import DocumentProcessor


class RAGSystem:
    """
    RAG system for document Q&A.

    Simple workflow:
    1. Index PDFs (extract text → chunk → embed → store)
    2. Query (embed question → search → generate answer)
    """

    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: str = "data/vector_store",
        embedding_model: str = "paraphrase-MiniLM-L3-v2",  # Smaller, faster model
    ):
        """
        Initialize RAG system.

        Args:
            collection_name: Name for the document collection
            persist_directory: Where to store vectors
            embedding_model: Sentence-transformers model name
        """
        # Check dependencies
        if chromadb is None:
            raise ImportError(
                "chromadb is required for RAG. Install with: pip install chromadb"
            )
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is required. "
                "Install with: pip install sentence-transformers"
            )

        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.doc_processor = DocumentProcessor()
        # Use CPU and optimize memory
        self.embedding_model = SentenceTransformer(
            embedding_model,
            device='cpu',  # Use CPU (more stable)
        )
        # Set to use less memory
        self.embedding_model.max_seq_length = 128  # Reduce sequence length

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},  # Cosine similarity
        )

    def index_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Index a PDF document.

        Args:
            file_path: Path to PDF file

        Returns:
            Indexing results with statistics

        Example:
            >>> rag = RAGSystem()
            >>> result = rag.index_document(Path("paper.pdf"))
            >>> print(f"Indexed {result['num_chunks']} chunks")
        """
        print(f"📄 Processing: {file_path.name}")

        # Step 1: Extract text from PDF
        doc_data = self.doc_processor.process_pdf(file_path)
        text = doc_data["text"]
        print(f"   ✓ Extracted {len(text)} characters")

        # Step 2: Chunk text
        chunks = self.doc_processor.chunk_text(text, chunk_size=500, overlap=50)
        print(f"   ✓ Created {len(chunks)} chunks")

        # Step 3: Generate embeddings
        print(f"   ⏳ Generating embeddings for {len(chunks)} chunks...")
        try:
            # Generate embeddings in smaller batches to avoid blocking
            embeddings = self.embedding_model.encode(
                chunks, 
                show_progress_bar=True,
                batch_size=8,  # Smaller batches for stability
                convert_to_numpy=True
            )
            print(f"   ✓ Generated {len(embeddings)} embeddings")
        except Exception as e:
            print(f"   ✗ Error generating embeddings: {e}")
            raise

        # Step 4: Store in vector database
        ids = [f"{file_path.stem}_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": str(file_path),
                "file_name": file_path.name,
                "chunk_index": i,
                "page_count": doc_data["metadata"]["page_count"],
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids, embeddings=embeddings.tolist(), documents=chunks, metadatas=metadatas
        )
        print(f"   ✓ Stored in vector database")

        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "num_chunks": len(chunks),
            "page_count": doc_data["metadata"]["page_count"],
        }

    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Query the RAG system.

        Args:
            question: User's question
            k: Number of chunks to retrieve

        Returns:
            Dictionary with answer context and sources

        Example:
            >>> rag = RAGSystem()
            >>> result = rag.query("What is RAG?")
            >>> print(result["context"])
        """
        # Embed question
        query_embedding = self.embedding_model.encode([question])[0]

        # Search vector database
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()], n_results=k
        )

        # Format results
        if not results["documents"] or not results["documents"][0]:
            return {
                "context": "",
                "sources": [],
                "chunks": [],
                "has_results": False,
            }

        # Build context from retrieved chunks
        chunks = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0] if "distances" in results else []

        # Extract unique sources
        sources = {}
        for meta in metadatas:
            source = meta.get("file_name", "Unknown")
            if source not in sources:
                sources[source] = {"file": source, "chunks": 0}
            sources[source]["chunks"] += 1

        # Build context string
        context_parts = []
        for i, (chunk, meta) in enumerate(zip(chunks, metadatas), 1):
            source = meta.get("file_name", "Unknown")
            chunk_idx = meta.get("chunk_index", 0)
            context_parts.append(f"[{i}] (Source: {source}, Chunk: {chunk_idx})\n{chunk}")

        context = "\n\n".join(context_parts)

        return {
            "context": context,
            "sources": list(sources.values()),
            "chunks": chunks,
            "has_results": True,
            "num_results": len(chunks),
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all indexed documents.

        Returns:
            List of documents with statistics
        """
        all_data = self.collection.get()

        if not all_data["metadatas"]:
            return []

        # Group by source
        docs = {}
        for meta in all_data["metadatas"]:
            source = meta.get("file_name", "Unknown")
            if source not in docs:
                docs[source] = {
                    "file_name": source,
                    "file_path": meta.get("source", ""),
                    "chunks": 0,
                    "pages": meta.get("page_count", 0),
                }
            docs[source]["chunks"] += 1

        return list(docs.values())

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
