# -*- coding: utf-8 -*-
"""
Simple RAG system using keyword search (no embeddings).

Fast, lightweight, works instantly!
Following Rule #1: Keep it simple.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from local_prompt_agent.document import DocumentProcessor


class SimpleRAG:
    """
    Simple RAG using keyword search instead of embeddings.

    Advantages:
    - No model download (works instantly!)
    - Low memory usage
    - Fast indexing (seconds, not minutes)
    - Good enough for most use cases
    """

    def __init__(self, persist_directory: str = "data/simple_rag"):
        """Initialize simple RAG."""
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.doc_processor = DocumentProcessor()
        self.index_file = self.persist_directory / "index.json"
        self.documents = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """Load index from disk."""
        if self.index_file.exists():
            with open(self.index_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_index(self) -> None:
        """Save index to disk."""
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)

    def index_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Index a PDF document.

        Fast! No embeddings needed.
        """
        print(f"📄 Processing: {file_path.name}")

        # Extract text
        doc_data = self.doc_processor.process_pdf(file_path)
        text = doc_data["text"]
        print(f"   ✓ Extracted {len(text)} characters")

        # Chunk text
        chunks = self.doc_processor.chunk_text(text, chunk_size=500, overlap=50)
        print(f"   ✓ Created {len(chunks)} chunks")

        # Store (no embeddings needed!)
        doc_id = file_path.stem
        self.documents[doc_id] = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "chunks": chunks,
            "page_count": doc_data["metadata"]["page_count"],
            "num_chunks": len(chunks),
        }

        self._save_index()
        print(f"   ✓ Indexed (keyword search)")

        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "num_chunks": len(chunks),
            "page_count": doc_data["metadata"]["page_count"],
        }

    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Query using keyword search.

        Fast and effective!
        """
        if not self.documents:
            return {
                "context": "",
                "sources": [],
                "chunks": [],
                "has_results": False,
            }

        # Extract keywords from question (simple: just lowercase words)
        keywords = set(re.findall(r'\w+', question.lower()))
        
        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = keywords - stopwords

        # Score each chunk
        scored_chunks = []
        for doc_id, doc in self.documents.items():
            for idx, chunk in enumerate(doc["chunks"]):
                # Count keyword matches
                chunk_lower = chunk.lower()
                score = sum(1 for kw in keywords if kw in chunk_lower)
                
                if score > 0:
                    scored_chunks.append({
                        "chunk": chunk,
                        "score": score,
                        "doc_id": doc_id,
                        "file_name": doc["file_name"],
                        "chunk_idx": idx,
                    })

        # Sort by score
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top K
        top_chunks = scored_chunks[:k]

        if not top_chunks:
            return {
                "context": "",
                "sources": [],
                "chunks": [],
                "has_results": False,
            }

        # Build context
        context_parts = []
        sources = {}
        
        for i, item in enumerate(top_chunks, 1):
            file_name = item["file_name"]
            chunk_idx = item["chunk_idx"]
            chunk = item["chunk"]
            
            context_parts.append(
                f"[{i}] (Source: {file_name}, Chunk: {chunk_idx})\n{chunk}"
            )
            
            if file_name not in sources:
                sources[file_name] = {"file": file_name, "chunks": 0}
            sources[file_name]["chunks"] += 1

        return {
            "context": "\n\n".join(context_parts),
            "sources": list(sources.values()),
            "chunks": [item["chunk"] for item in top_chunks],
            "has_results": True,
            "num_results": len(top_chunks),
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        """List all indexed documents."""
        return [
            {
                "file_name": doc["file_name"],
                "file_path": doc["file_path"],
                "chunks": doc["num_chunks"],
                "pages": doc["page_count"],
            }
            for doc in self.documents.values()
        ]

    def clear(self) -> None:
        """Clear all indexed documents."""
        self.documents = {}
        self._save_index()
