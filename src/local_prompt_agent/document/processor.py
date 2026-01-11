# -*- coding: utf-8 -*-
"""
PDF document processor.

Simple PDF text extraction following Rule #1: Keep it simple.
"""

from pathlib import Path
from typing import Dict, List, Optional

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class DocumentProcessor:
    """Process PDF documents and extract text."""

    def __init__(self):
        """Initialize document processor."""
        if pdfplumber is None:
            raise ImportError(
                "pdfplumber is required for PDF processing. "
                "Install with: pip install pdfplumber"
            )

    def process_pdf(self, file_path: Path) -> Dict[str, any]:
        """
        Extract text from PDF.

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with text and metadata

        Example:
            >>> processor = DocumentProcessor()
            >>> result = processor.process_pdf("paper.pdf")
            >>> print(result["text"])
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        pages_text = []
        metadata = {}

        with pdfplumber.open(file_path) as pdf:
            # Extract metadata
            metadata = {
                "page_count": len(pdf.pages),
                "file_name": file_path.name,
                "file_path": str(file_path),
            }

            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    pages_text.append({"page": page_num, "text": text})

        # Combine all pages
        full_text = "\n\n".join([p["text"] for p in pages_text if p["text"]])

        return {
            "text": full_text,
            "pages": pages_text,
            "metadata": metadata,
        }

    def chunk_text(
        self, text: str, chunk_size: int = 500, overlap: int = 50
    ) -> List[str]:
        """
        Split text into chunks with overlap.

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        if not text:
            return []

        print(f"   ⏳ Chunking {len(text)} characters...")
        
        chunks = []
        start = 0
        
        # Estimate number of chunks
        estimated_chunks = len(text) // (chunk_size - overlap) + 1
        print(f"   ⏳ Creating ~{estimated_chunks} chunks...")

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Try to break at sentence boundary (limit search to avoid slow rfind)
            if end < len(text):
                # Search only in last 100 chars for efficiency
                search_start = max(start, end - 100)
                for delimiter in ["\n\n", "。", ".", "!", "?", "\n"]:
                    last_pos = text.rfind(delimiter, search_start, end)
                    if last_pos > start:
                        end = last_pos + 1
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start with overlap
            start = end - overlap if end < len(text) else len(text)
            
            # Avoid infinite loop
            if start >= len(text):
                break

        print(f"   ✓ Created {len(chunks)} chunks")
        return chunks
