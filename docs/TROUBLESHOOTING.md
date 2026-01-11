# Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Issue: Server Killed During PDF Upload

**Symptoms:**
```
📄 Processing: document.pdf
   ✓ Extracted 62354 characters
zsh: killed     lpa serve
```

**Cause:** Memory exhaustion during embedding generation (first-time model download + processing).

**Solutions:**

#### Solution 1: Use Lighter Model (Already Fixed! ✅)
We've updated to use a smaller, faster model:
- **Before**: `all-MiniLM-L6-v2` (~80MB, 384 dimensions)
- **After**: `paraphrase-MiniLM-L3-v2` (~60MB, 384 dimensions, faster)

Just pull latest code and restart:
```bash
git pull origin main
lpa serve
```

#### Solution 2: Increase Memory Limit (macOS/Linux)
```bash
# Check current limit
ulimit -m

# Increase to 4GB
ulimit -m 4194304

# Then restart
lpa serve
```

#### Solution 3: Process PDFs via CLI First
If Web UI still has issues, use CLI (uses less memory):
```bash
# Index via CLI (more memory-efficient)
lpa rag index your_document.pdf

# Then use Web UI for questions
lpa serve
# Toggle RAG Mode ON in browser
```

#### Solution 4: Use Smaller PDFs
- Split large PDFs into smaller files
- Or process one at a time

---

### Issue: "Cannot connect to backend"

**Symptoms:**
```
Warning: Cannot connect to backend
```

**Cause:** Ollama not running.

**Solution:**
```bash
# Start Ollama
ollama serve

# In another terminal
lpa chat
```

---

### Issue: "Model not found"

**Symptoms:**
```
Error: model 'mistral' not found
```

**Cause:** Model not downloaded.

**Solution:**
```bash
# Pull the model
ollama pull mistral

# Or use different model
ollama pull llama2
```

---

### Issue: "Module not found: pdfplumber"

**Symptoms:**
```
ImportError: pdfplumber is required
```

**Cause:** RAG dependencies not installed.

**Solution:**
```bash
pip install pdfplumber sentence-transformers chromadb
```

---

### Issue: Web UI Not Loading

**Symptoms:**
- Blank page
- 404 errors

**Solutions:**

1. **Check server is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

2. **Check correct port:**
```bash
lpa serve --port 8000
# Visit: http://localhost:8000 (not 8080)
```

3. **Check firewall:**
```bash
# Try 127.0.0.1 instead of localhost
http://127.0.0.1:8000
```

---

### Issue: Chinese Characters Garbled

**Symptoms:**
```
你好 shows as ä½ å¥½
```

**Cause:** Encoding issue.

**Solution:**
Should not happen (we have UTF-8 everywhere), but if it does:

1. **Check browser encoding:** View → Encoding → UTF-8
2. **Clear browser cache:** Cmd+Shift+R (hard reload)
3. **Check config file encoding:** Must be saved as UTF-8

---

### Issue: RAG Not Finding Relevant Content

**Symptoms:**
- "No documents indexed"
- Irrelevant answers

**Solutions:**

1. **Verify documents are indexed:**
```bash
lpa rag list
# Should show your PDFs
```

2. **Check RAG mode is enabled:**
- CLI: Use `lpa chat --rag`
- Web UI: Toggle "RAG Mode" ON (switch should be blue)

3. **Ask more specific questions:**
```
❌ Bad: "Tell me about it"
✅ Good: "What are the key findings in the methodology section?"
```

4. **Increase top-k:**
```bash
lpa rag query "your question" --top-k 10
# Retrieves more chunks
```

---

### Issue: Slow Performance

**Symptoms:**
- Long wait times
- Slow responses

**Solutions:**

1. **Use smaller model (Ollama):**
```bash
ollama pull phi  # 2.7B, much faster
# Edit config: model: "phi"
```

2. **Reduce max_tokens:**
```yaml
# config/config.yaml
backend:
  max_tokens: 1024  # Instead of 2048
```

3. **Use CPU only (no GPU issues):**
Already configured for CPU by default.

---

### Issue: "Address already in use"

**Symptoms:**
```
Error: listen tcp 127.0.0.1:8000: bind: address already in use
```

**Cause:** Server already running on that port.

**Solutions:**

1. **Use different port:**
```bash
lpa serve --port 8080
```

2. **Kill existing process:**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

3. **It's actually fine!** 
If Ollama says "address already in use", it means it's already running (which is good).

---

### Issue: Upload Progress Stuck

**Symptoms:**
- "Uploading..." never completes
- Spinner forever

**Solutions:**

1. **Check file size:**
- Large PDFs (>50MB) take time
- Wait 1-2 minutes
- Check terminal for progress

2. **Try CLI instead:**
```bash
lpa rag index your_document.pdf
# Then refresh Web UI
```

3. **Check logs:**
Look at terminal running `lpa serve` for error messages.

---

## 💡 Performance Tips

### For Better Performance

1. **Use appropriate models:**
   - **Fast**: `phi` (Ollama)
   - **Balanced**: `mistral` (Ollama)
   - **Quality**: `gpt-4` (OpenAI, requires API key)

2. **Optimize chunk size:**
```yaml
# Smaller chunks = faster but less context
chunk_size: 300  # Instead of 500
```

3. **Process PDFs ahead of time:**
```bash
# Index all PDFs before using Web UI
lpa rag index *.pdf
```

---

## 🔍 Debugging Commands

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Check API health
curl http://localhost:8000/health

# List Ollama models
ollama list

# List indexed documents
lpa rag list

# Test configuration
lpa config

# Check Python version
python3 --version  # Should be 3.9+

# Check installation
pip list | grep local-prompt-agent
```

---

## 📞 Getting Help

### If Issues Persist

1. **Check logs:** Terminal output from `lpa serve`
2. **Check GitHub Issues:** https://github.com/patrick-ckf/local-prompt-agent/issues
3. **Include details:**
   - Error message
   - Python version
   - OS (macOS/Linux/Windows)
   - PDF size
   - Steps to reproduce

---

## 🎯 Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Server killed | Use `git pull` (fixed in latest) |
| Backend connection | `ollama serve` |
| Model not found | `ollama pull mistral` |
| RAG dependencies | `pip install pdfplumber sentence-transformers chromadb` |
| Web UI not loading | Check `http://localhost:8000` |
| Slow performance | Use `phi` model |
| Port in use | `lpa serve --port 8080` |
| Upload stuck | Try `lpa rag index file.pdf` in CLI |

---

**Most issues have simple solutions! Check above first.** 🔧
