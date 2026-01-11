# Getting Started with Local Prompt Agent

🎉 **Phase 1 Implementation is Complete!** You can now run a basic local AI assistant.

## ✅ What's Implemented

### Phase 1 (Complete) ✅
- ✅ Core Agent class
- ✅ Ollama backend (local LLMs)
- ✅ Configuration system (YAML + Pydantic)
- ✅ Interactive CLI with Rich formatting
- ✅ Streaming responses
- ✅ Conversation history
- ✅ Basic tests

### Phase 2 (Complete) ✅
- ✅ REST API with FastAPI
- ✅ **Modern Web UI** (ChatGPT-style interface)
- ✅ WebSocket streaming
- ✅ Light/Dark mode
- ✅ Mobile responsive design
- ✅ Multi-language UI support

### Phase 3 (Complete) ✅
- ✅ **PDF Document Processing** (pdfplumber)
- ✅ **RAG System** (Retrieval-Augmented Generation)
- ✅ **Semantic Search** (ChromaDB + embeddings)
- ✅ **Question Answering** with citations
- ✅ CLI commands (`rag index`, `rag query`, `rag list`)
- ✅ Multi-document support

### Phase 4 (Complete) ✅
- ✅ **OpenAI Backend** (GPT-4, GPT-3.5-turbo)
- ✅ **Anthropic Backend** (Claude 3 Opus/Sonnet/Haiku)
- ✅ **Tool System** (function calling)
- ✅ **Built-in Tools** (calculator, file_read)
- ✅ **Multi-Backend Switching** (Ollama/OpenAI/Claude)

## 📋 Prerequisites

### 1. Python 3.11 or Higher

```bash
python3 --version  # Should be 3.11+
```

### 2. Ollama (for Local LLMs)

Download and install Ollama from: https://ollama.ai

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 3. Pull a Model

```bash
# Pull Mistral (recommended, ~4GB)
ollama pull mistral

# Or other models:
ollama pull llama2        # Meta's Llama 2
ollama pull codellama     # Code-focused
ollama pull phi           # Small, fast (2GB)
```

## 🚀 Installation

### Step 1: Clone the Repository

```bash
cd ~/codes  # Or your preferred directory
git clone https://github.com/patrick-ckf/local-prompt-agent.git
cd local-prompt-agent
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python3.11 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# Or on Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install in development mode
pip install -e .

# Or install with all optional dependencies
pip install -e ".[all]"
```

## 🎮 Usage

### 1. Start Ollama (if not running)

```bash
# Start Ollama server
ollama serve
```

Leave this running in a terminal.

### 2. Option A: Web UI (Recommended) 🌐

```bash
# Start the API server with Web UI
lpa serve

# Or custom port
lpa serve --port 8080
```

Then open your browser to: **http://localhost:8000**

**Features**:
- ✨ Modern ChatGPT-style interface
- ⚡ Real-time streaming responses
- 🌓 Light/Dark mode toggle
- 📱 Mobile responsive
- 🌐 Multi-language (EN, 繁體中文, 简体中文)
- 🎯 Suggested prompts
- 💬 Beautiful message bubbles

### 3. Option B: Interactive CLI

```bash
# Start chat in terminal
local-prompt-agent chat

# Or use short command
lpa chat
```

### 4. Option C: RAG - Ask Questions About PDFs 📄

```bash
# Install RAG dependencies first
pip install pdfplumber sentence-transformers chromadb

# Index your PDF documents
lpa rag index research_paper.pdf
lpa rag index contract.pdf

# List indexed documents
lpa rag list

# Ask questions about your documents
lpa rag query "What are the key findings?"

# Or chat with RAG mode
lpa chat --rag
```

**See [RAG_QUICKSTART.md](docs/RAG_QUICKSTART.md) for complete guide!**

### 5. Use Cloud LLMs (OpenAI/Claude) 🚀

```bash
# Set API key
export OPENAI_API_KEY="sk-proj-..."
# OR
export ANTHROPIC_API_KEY="sk-ant-..."

# Edit config/config.yaml:
# backend:
#   type: "openai"     # or "anthropic"
#   model: "gpt-4"     # or "claude-3-opus-20240229"

# Chat with cloud LLMs
lpa chat
```

**See [BACKENDS_GUIDE.md](docs/BACKENDS_GUIDE.md) for complete guide!**

### 6. Use Tools (Calculator, File Ops) 🛠️

Tools allow the agent to perform actions:

```python
from local_prompt_agent.tools.builtin import CalculatorTool, FileReadTool

# Calculator
calc = CalculatorTool()
result = await calc.execute(expression="25 * 4 + 10")
# Result: 110

# File read
file_tool = FileReadTool()
result = await file_tool.execute(file_path="README.md")
# Returns file contents
```

**See [TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md) for complete guide!**

**Commands in chat**:
- Type your message and press Enter
- `/exit` - Quit
- `/clear` - Clear conversation history
- `/help` - Show help

**Example**:
```
You: Hello! How does RAG work?
Assistant: RAG (Retrieval-Augmented Generation) is...

You: Can you explain it in Chinese?
Assistant: RAG（检索增强生成）是...
```

### 3. Configuration

Edit `config/config.yaml`:

```yaml
system:
  language: "zh-TW"  # Change to zh-TW or zh-CN for Chinese

backend:
  model: "mistral"  # Change model
  temperature: 0.7  # Creativity (0.0-1.0)
  max_tokens: 2048  # Response length
```

### 4. View Configuration

```bash
lpa config
```

### 5. Check Version

```bash
lpa version
```

## 🧪 Testing

Run tests:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest

# With coverage
pytest --cov
```

## 📖 Examples

### Example 1: Simple Question

```bash
lpa chat
```
```
You: What is Python?
Assistant: Python is a high-level programming language...
```

### Example 2: Code Generation

```
You: Write a Python function to calculate fibonacci
Assistant: Here's a Python function:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Example 3: Multi-language Support

```
You: 用繁體中文解釋什麼是AI
Assistant: AI（人工智慧）是指...
```

## 🔧 Troubleshooting

### "Cannot connect to backend"

**Problem**: Ollama is not running

**Solution**:
```bash
# Start Ollama
ollama serve

# In another terminal, check if running
curl http://localhost:11434/api/tags
```

### "Model not found"

**Problem**: Model not downloaded

**Solution**:
```bash
# List installed models
ollama list

# Pull the model
ollama pull mistral
```

### "Module not found"

**Problem**: Package not installed correctly

**Solution**:
```bash
# Reinstall
pip install -e .
```

## 🎨 Customization

### Change Model

Edit `config/config.yaml`:
```yaml
backend:
  model: "llama2"  # or codellama, phi, etc.
```

Or override in command:
```bash
lpa chat --model llama2
```

### Change Temperature

More creative (higher) or more focused (lower):
```yaml
backend:
  temperature: 0.3  # Focused (good for code)
  # or
  temperature: 0.9  # Creative (good for stories)
```

### Disable Streaming

For complete responses:
```bash
lpa chat --no-stream
```

## 📊 Project Structure

```
local-prompt-agent/
├── src/local_prompt_agent/
│   ├── __init__.py
│   ├── agent.py           # Core Agent class
│   ├── backends/
│   │   ├── base.py        # Base backend interface
│   │   └── ollama.py      # Ollama implementation
│   ├── cli/
│   │   └── main.py        # CLI interface
│   └── config/
│       └── settings.py    # Configuration
├── tests/
│   └── test_config.py     # Basic tests
├── config/
│   └── config.yaml        # Configuration file
├── pyproject.toml         # Project metadata
└── README.md
```

## 🚀 Next Steps

### Phase 2: Coming Soon
- REST API (FastAPI)
- Document processing (PDF, DOCX)
- RAG system (ChromaDB)
- Web UI
- Multi-agent support

### Contributing

Want to help implement Phase 2? Check out the specifications in `specs/` directory!

## 📚 Documentation

- **Full Specification**: `specs/specification.adoc`
- **RAG Design**: `specs/pdf-rag-design.adoc`
- **Multi-Agent**: `specs/multi-agent-enhancement.adoc`
- **i18n Support**: `specs/i18n-enhancement.adoc`
- **Web UI Design**: `specs/web-ui-design.adoc`

## 💡 Tips

1. **Start Ollama first** before running the agent
2. **Use smaller models** (phi) for faster responses
3. **Adjust temperature** based on your needs
4. **Clear history** (`/clear`) for unrelated topics
5. **Check config** (`lpa config`) if something's wrong

## ❓ FAQ

**Q: Which model should I use?**  
A: Start with `mistral` (balanced) or `phi` (fast). For code, use `codellama`.

**Q: Can I use OpenAI/Claude?**  
A: Phase 1 supports Ollama only. OpenAI/Claude coming in Phase 2.

**Q: Does it work offline?**  
A: Yes! With Ollama, everything runs locally offline.

**Q: Is it free?**  
A: Yes! Completely free and open source.

**Q: What about my data?**  
A: Everything stays on your machine. Privacy-first!

---

**🎉 You're all set! Start chatting with your local AI assistant!**

```bash
lpa chat
```

**Need help?** Open an issue on GitHub: https://github.com/patrick-ckf/local-prompt-agent/issues
