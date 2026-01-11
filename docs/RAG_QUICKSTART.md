# RAG Quick Start - Ask Questions About Your PDFs

## 🎯 What is RAG?

**RAG (Retrieval-Augmented Generation)** lets you ask questions about your PDF documents. The agent reads your PDFs, finds relevant information, and answers based on the content.

## 📚 Use Cases

- **Research**: "What are the key findings in this paper?"
- **Contracts**: "What are the payment terms?"
- **Manuals**: "How do I configure the database?"
- **Reports**: "Summarize the Q4 results"
- **Books**: "What does the author say about AI?"

## 🚀 Quick Start

### Step 1: Install RAG Dependencies

```bash
cd /Users/patrickcheung/codes/local-prompt-agent
source venv/bin/activate

# Install RAG packages
pip install pdfplumber sentence-transformers chromadb
```

### Step 2: Index Your PDF

```bash
# Index a single PDF
lpa rag index path/to/your/document.pdf

# Index multiple PDFs
lpa rag index paper1.pdf
lpa rag index paper2.pdf
lpa rag index contract.pdf
```

**Output**:
```
📄 Processing: research_paper.pdf
   ✓ Extracted 15,234 characters
   ✓ Created 32 chunks
   ⏳ Generating embeddings...
   ✓ Generated embeddings
   ✓ Stored in vector database

╭──────── Indexing Complete ────────╮
│ ✓ Document indexed successfully   │
│                                   │
│ File: research_paper.pdf          │
│ Pages: 12                         │
│ Chunks: 32                        │
╰───────────────────────────────────╯
```

### Step 3: List Indexed Documents

```bash
lpa rag list
```

**Output**:
```
╭───── Indexed Documents ─────╮

research_paper.pdf
  Path: /path/to/research_paper.pdf
  Pages: 12
  Chunks: 32

contract.pdf
  Path: /path/to/contract.pdf
  Pages: 8
  Chunks: 18
```

### Step 4: Ask Questions

**Option A: Direct Query** (Quick)
```bash
lpa rag query "What are the key findings?"
```

**Option B: Chat with RAG** (Interactive)
```bash
lpa chat --rag
```

Then ask questions normally:
```
You: What are the main conclusions in the paper?
Assistant: Based on the research paper, the main conclusions are...

Sources:
- research_paper.pdf
```

## 💡 Examples

### Example 1: Research Paper

```bash
# Index research paper
lpa rag index research_paper.pdf

# Ask questions
lpa rag query "What methodology was used?"
lpa rag query "What are the limitations?"
lpa rag query "Who are the authors?"
```

### Example 2: Multiple Documents

```bash
# Index multiple papers
lpa rag index paper1.pdf
lpa rag index paper2.pdf
lpa rag index paper3.pdf

# Compare across documents
lpa chat --rag
You: Compare the methodologies across all papers
Assistant: Based on the three papers... [cites all sources]
```

### Example 3: Interactive RAG Chat

```bash
lpa chat --rag

You: What does the contract say about termination?
Assistant: According to the contract, termination requires...
Sources:
- contract.pdf

You: And what about the payment schedule?
Assistant: The payment schedule specifies...
Sources:
- contract.pdf

You: 用繁體中文總結合約要點
Assistant: 根據合約，主要要點包括...
來源：
- contract.pdf
```

## 🎨 Web UI with RAG

Start the web server:
```bash
lpa serve
```

Then visit: **http://localhost:8000**

*Note: Web UI RAG integration coming soon - for now use CLI*

## 🔧 Advanced Usage

### Custom Chunk Size

Edit `config/config.yaml`:
```yaml
rag:
  chunk_size: 500     # Characters per chunk
  overlap: 50         # Overlap between chunks
  top_k: 5           # Number of chunks to retrieve
```

### Query with More Context

```bash
# Retrieve more chunks for complex questions
lpa rag query "Explain the entire methodology" --top-k 10
```

## 🧹 Maintenance

### Clear All Indexed Documents

```bash
# Delete the vector store
rm -rf data/vector_store

# Or programmatically (coming soon)
lpa rag clear
```

## ⚡ Performance

**First-time setup** (~1-2 minutes):
- Downloads embedding model (~80MB)
- One-time download, then cached

**Indexing**:
- Small PDF (10 pages): ~5-10 seconds
- Large PDF (100 pages): ~30-60 seconds

**Querying**:
- Question → Answer: ~1-2 seconds
- All processing local (private!)

## 🌐 Supported Languages

PDFs in any language work:
- English
- Traditional Chinese (繁體中文)
- Simplified Chinese (简体中文)
- Spanish, French, German, etc.

Ask questions in any language too!

## 💡 Tips

1. **Index First**: Always index before asking questions
2. **Descriptive Questions**: Ask specific questions for better answers
3. **Multiple Documents**: Index all related PDFs for comprehensive answers
4. **Check Sources**: Always verify the cited sources
5. **Re-index**: If PDF changes, re-index it

## ❓ Troubleshooting

### "No documents indexed"

**Solution**: Index a PDF first
```bash
lpa rag index your_document.pdf
```

### "Module not found: pdfplumber"

**Solution**: Install RAG dependencies
```bash
pip install pdfplumber sentence-transformers chromadb
```

### "Slow embedding generation"

**Solution**: First run downloads model (~80MB), then it's fast

---

## 🎉 You're Ready!

Now you can ask questions about your PDF documents!

```bash
# 1. Index your PDF
lpa rag index my_document.pdf

# 2. Ask questions
lpa chat --rag

# 3. Get answers with citations!
```

**Your documents stay private - everything runs locally!** 🔒
