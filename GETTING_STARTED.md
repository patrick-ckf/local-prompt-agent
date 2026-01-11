# Getting Started with Local Prompt Agent

🎉 **Phase 1 Implementation is Complete!** You can now run a basic local AI assistant.

## ✅ What's Implemented (Phase 1)

- ✅ Core Agent class
- ✅ Ollama backend (local LLMs)
- ✅ Configuration system (YAML + Pydantic)
- ✅ Interactive CLI with Rich formatting
- ✅ Streaming responses
- ✅ Conversation history
- ✅ Basic tests

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

### 2. Interactive Chat

```bash
# Start chat
local-prompt-agent chat

# Or use short command
lpa chat
```

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
