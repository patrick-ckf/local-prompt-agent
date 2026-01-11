# Backend Guide - Ollama, OpenAI, Claude

## 📚 Supported Backends

The Local Prompt Agent supports **3 LLM backends**:

1. **Ollama** - Local, free, private (default)
2. **OpenAI** - Cloud, paid, powerful (GPT-4)
3. **Anthropic** - Cloud, paid, excellent (Claude 3)

## 🎯 Quick Comparison

| Backend | Cost | Privacy | Speed | Quality | Setup |
|---------|------|---------|-------|---------|-------|
| **Ollama** | Free | 100% Private | Fast | Good | Easy |
| **OpenAI** | Paid | Cloud | Fast | Excellent | API Key |
| **Anthropic** | Paid | Cloud | Fast | Excellent | API Key |

## 🚀 1. Ollama (Default - Local & Free)

### Setup

```bash
# Install Ollama
brew install ollama  # macOS

# Pull a model
ollama pull mistral
ollama pull llama2
ollama pull codellama

# Start Ollama
ollama serve
```

### Configuration

`config/config.yaml`:
```yaml
backend:
  type: "ollama"
  base_url: "http://localhost:11434"
  model: "mistral"  # or llama2, codellama, phi, gemma
  temperature: 0.7
  max_tokens: 2048
```

### Usage

```bash
# Use default (Ollama)
lpa chat

# Specify model
lpa chat --model llama2
lpa chat --model codellama
```

### Models Available

- `mistral` - Balanced, good all-around (7B)
- `llama2` - Meta's model (7B, 13B, 70B)
- `codellama` - Code-focused (7B, 13B)
- `phi` - Small and fast (2.7B)
- `gemma` - Google's model (2B, 7B)

**See all**: `ollama list`

---

## 💰 2. OpenAI (Cloud - GPT-4)

### Setup

```bash
# Get API key from: https://platform.openai.com/api-keys

# Set environment variable
export OPENAI_API_KEY="sk-proj-..."

# Or add to ~/.zshrc or ~/.bashrc
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.zshrc
```

### Configuration

`config/config.yaml`:
```yaml
backend:
  type: "openai"
  model: "gpt-4"  # or gpt-4-turbo, gpt-3.5-turbo
  api_key: null  # Will use OPENAI_API_KEY env var
  temperature: 0.7
  max_tokens: 2048
```

### Usage

```bash
# Edit config.yaml to use OpenAI, then:
lpa chat

# Or override in command (coming soon)
lpa chat --backend openai --model gpt-4
```

### Models Available

- `gpt-4` - Most capable ($0.03/1K tokens)
- `gpt-4-turbo` - Faster, cheaper ($0.01/1K tokens)
- `gpt-3.5-turbo` - Fast, affordable ($0.0005/1K tokens)

**Pricing**: https://openai.com/pricing

---

## 🤖 3. Anthropic Claude (Cloud)

### Setup

```bash
# Get API key from: https://console.anthropic.com/

# Install anthropic package
pip install anthropic

# Set environment variable
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Configuration

`config/config.yaml`:
```yaml
backend:
  type: "anthropic"
  model: "claude-3-opus-20240229"
  api_key: null  # Will use ANTHROPIC_API_KEY env var
  temperature: 0.7
  max_tokens: 2048
```

### Usage

```bash
# Edit config.yaml to use Anthropic, then:
lpa chat
```

### Models Available

- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fast, affordable

---

## 🔄 Switching Backends

### Method 1: Edit Config (Permanent)

Edit `config/config.yaml` and change the `type`:

```yaml
backend:
  type: "openai"  # Change this
  model: "gpt-4"   # And this
  api_key: null
```

### Method 2: Environment Variable (Temporary)

```bash
# Use OpenAI for this session
export LPA_BACKEND__TYPE="openai"
export LPA_BACKEND__MODEL="gpt-4"

lpa chat
```

### Method 3: Multiple Configs (Organized)

Create different config files:

```bash
# config/ollama.yaml
backend:
  type: "ollama"
  model: "mistral"

# config/openai.yaml
backend:
  type: "openai"
  model: "gpt-4"
  api_key: "sk-..."
```

Use with:
```bash
lpa --config config/ollama.yaml chat
lpa --config config/openai.yaml chat
```

---

## 💡 When to Use Which Backend

### Use **Ollama** when:
- ✅ You want privacy (100% local)
- ✅ No cost matters
- ✅ No internet access
- ✅ Experimenting and learning
- ✅ Sensitive documents

### Use **OpenAI** when:
- ✅ Need best quality (GPT-4)
- ✅ Complex reasoning required
- ✅ Large context windows needed
- ✅ Cost not a concern

### Use **Anthropic Claude** when:
- ✅ Need long context (200K tokens)
- ✅ Want ethical AI
- ✅ Complex analysis tasks
- ✅ Excellent instruction following

---

## 🔒 API Key Security

### Best Practices

1. **Never commit API keys to git!**
2. **Use environment variables**
3. **Use .env files (gitignored)**

### Using .env File

Create `.env` in project root (gitignored):
```bash
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

The agent will automatically load these.

---

## 💵 Cost Comparison

### Ollama (Free)
- **Cost**: $0
- **Privacy**: 100%
- **Speed**: Fast
- **Needs**: Local GPU/CPU

### OpenAI GPT-4
- **Cost**: ~$0.03 per 1K tokens (~$0.06 per page)
- **Privacy**: Cloud
- **Speed**: Fast
- **Quality**: Excellent

### Anthropic Claude
- **Cost**: Similar to GPT-4
- **Privacy**: Cloud
- **Speed**: Fast
- **Context**: Up to 200K tokens

---

## 🧪 Testing Different Backends

```bash
# Test with Ollama (free)
lpa chat
You: Explain quantum computing

# Test with OpenAI (after setting API key)
# Edit config.yaml: type: "openai", model: "gpt-4"
lpa chat
You: Explain quantum computing

# Compare responses!
```

---

## ❓ FAQ

**Q: Can I use multiple backends at once?**  
A: Not yet, but multi-agent system (Phase 5) will support this.

**Q: Which is best for coding?**  
A: CodeLlama (Ollama) or GPT-4 (OpenAI)

**Q: Which supports Chinese best?**  
A: All support Chinese! Ollama models work great.

**Q: Do I need API keys for Ollama?**  
A: No! Ollama is completely free and local.

**Q: Can I switch mid-conversation?**  
A: Currently need to restart. Coming in future update.

---

## 🎯 Recommended Setup

### For Most Users (Privacy + Free)
```yaml
backend:
  type: "ollama"
  model: "mistral"
```

### For Best Quality (Cost OK)
```yaml
backend:
  type: "openai"
  model: "gpt-4-turbo"
  api_key: "set-as-env-var"
```

### For Long Documents (Need context)
```yaml
backend:
  type: "anthropic"
  model: "claude-3-opus-20240229"
  api_key: "set-as-env-var"
```

---

**See `config/config.yaml` for complete configuration options!**
