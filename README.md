# Local Prompt Agent

A sophisticated, locally-hosted intelligent agent system designed to manage, optimize, and execute AI prompts against local or remote Large Language Models (LLMs).

## 🎯 Key Features

- **Multi-Backend Support**: Compatible with Ollama, llama.cpp, LocalAI, OpenAI-compatible APIs
- **Document Processing & RAG**: Read and query PDFs, DOCX, and other documents with semantic search
- **Multi-Agent System**: Multiple specialized agents with different models and capabilities
- **Conversation Management**: Maintains context across interactions with intelligent memory strategies
- **Tool Integration**: Extensible architecture for custom tools and functions
- **Privacy-First**: All data processing occurs locally with optional encrypted storage

## 📁 Project Structure

```
local-prompt-agent/
├── specs/                  # Technical specifications (AsciiDoc)
│   ├── specification.adoc           # Main specification
│   ├── pdf-rag-design.adoc         # PDF/RAG system design
│   └── multi-agent-enhancement.adoc # Multi-agent architecture
├── summary/                # Summary documents (Markdown)
│   └── UPDATES_SUMMARY.md          # Updates and changes summary
├── temp/                   # Temporary files (not in git)
├── src/                    # Source code (to be implemented)
├── tests/                  # Test suite (to be implemented)
└── README.md              # This file
```

## 📚 Documentation

### Specifications (in `specs/`)

1. **[specification.adoc](specs/specification.adoc)** - Main technical specification
   - Overview and architecture
   - Functional & non-functional requirements
   - Document processing & RAG capabilities
   - Pseudo code and algorithms
   - Test cases and error handling
   - Recommended tech stack: **Python 3.11+**

2. **[pdf-rag-design.adoc](specs/pdf-rag-design.adoc)** - Detailed RAG system design
   - Document processing pipeline
   - Chunking strategies
   - Embedding generation
   - Vector storage and retrieval
   - Complete implementation examples

3. **[multi-agent-enhancement.adoc](specs/multi-agent-enhancement.adoc)** - Multi-agent architecture
   - Multiple specialized agents
   - Each agent with different models
   - Agent orchestration and routing
   - Model comparison and collaboration

### Summaries (in `summary/`)

- **[UPDATES_SUMMARY.md](summary/UPDATES_SUMMARY.md)** - Complete overview of all features and changes

## 🚀 Quick Start

### Phase 1: Review Specifications
```bash
# View main specification
cd specs/
asciidoc specification.adoc

# Or use any AsciiDoc viewer/converter
```

### Phase 2: Implementation (Coming Soon)
```bash
# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config.example.yaml config.yaml

# Run the agent
agent chat "Hello, world!"
```

## 🛠️ Tech Stack

**Language**: Python 3.11+

**Core Libraries**:
- FastAPI (REST API)
- Click (CLI)
- SQLAlchemy (Database)
- Pydantic (Validation)

**AI/ML**:
- ollama-python, llama-cpp-python (Local LLMs)
- sentence-transformers (Embeddings)
- OpenAI, Anthropic (Cloud APIs)

**Document Processing**:
- pdfplumber, PyMuPDF (PDF)
- python-docx (Word)
- pytesseract (OCR)

**RAG/Vectors**:
- ChromaDB (Vector database)
- FAISS (Similarity search)
- LangChain (RAG utilities)

## 💡 Use Cases

### 1. Research Assistant
```bash
agent rag index research_paper.pdf
agent chat "What are the key findings?"
```

### 2. Code Expert
```bash
agent chat --agent code_expert "Debug this Python function"
```

### 3. Multi-Document Analysis
```bash
agent chat "Compare the conclusions across all indexed papers"
```

### 4. Multi-Model Comparison
```bash
agent chat --compare "mistral,gpt-4,claude" "Explain quantum computing"
```

## 🎯 Current Status

✅ **Specifications Complete**
- Main architecture and requirements defined
- Document processing and RAG system designed
- Multi-agent architecture planned
- Complete pseudo code provided
- Test cases specified

🔄 **In Progress**
- Implementation Phase 1: Core components
- Setting up project structure
- Initial development

⏳ **Coming Soon**
- Full implementation
- Testing and optimization
- Documentation and examples
- Docker deployment

## 📖 How to Read the Specs

1. **Start with**: `specs/specification.adoc` - Main document with all requirements
2. **For RAG details**: `specs/pdf-rag-design.adoc` - Deep dive into document processing
3. **For multi-agent**: `specs/multi-agent-enhancement.adoc` - Agent architecture
4. **For quick overview**: `summary/UPDATES_SUMMARY.md` - Summary of all features

## 🤝 Contributing

(To be defined after Phase 1 implementation)

## 📄 License

(To be determined)

## 🔗 Resources

- Python 3.11+: https://www.python.org/
- Ollama: https://ollama.ai/
- ChromaDB: https://www.trychroma.com/
- LangChain: https://python.langchain.com/

---

**Version**: 1.0.0 (Specification Phase)  
**Author**: Patrick Cheung  
**Last Updated**: January 2026
