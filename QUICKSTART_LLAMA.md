# Quick Start: Llama 3.2 Setup for PyTestGenie

## 5-Minute Setup Guide

### Step 1: Install Ollama
**Windows**:
```powershell
# Download and install from https://ollama.ai
# Or use winget:
winget install Ollama.Ollama
```

**Linux/Mac**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Pull Llama 3.2 Model
```bash
ollama pull llama3.2
```
This downloads ~2GB of data. Wait for completion.

### Step 3: Verify Installation
```bash
# Check if model is available
ollama list

# Test the model
ollama run llama3.2 "Write a Python function to add two numbers"
```

Expected output: Should show llama3.2 in the list and generate Python code.

### Step 4: Start Your PyTestGenie Server
```bash
# Backend
cd backend
python app_unified.py

# Frontend (in another terminal)
cd frontend
npm install  # if first time
npm run dev
```

### Step 5: Generate Tests with Llama 3.2
1. Open browser: http://localhost:5173
2. Go to **Test Generator** tab
3. Select **"🧠 AI (OpenAI/HuggingFace)"**
4. From **"🤖 AI Model"** dropdown, choose **"Llama 3.2 (Local)"**
5. Paste this sample code:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
6. Click **"🚀 Generate Tests"**

### That's It! 🎉

You should see pytest test code generated using your local Llama 3.2 model.

## Troubleshooting

### Problem: "Connection refused to Llama server"
**Solution**:
```bash
# Check if Ollama is running
ollama serve

# On some systems, it may need manual start
```

### Problem: "Model llama3.2 not found"
**Solution**:
```bash
# Pull the model again
ollama pull llama3.2

# Verify it's downloaded
ollama list
```

### Problem: "Generation is slow"
**Causes**:
- First run: Model is loading into memory (wait 10-30 seconds)
- Low RAM: Llama needs ~8GB RAM
- CPU-only: No GPU acceleration

**Solutions**:
- Wait for first generation to complete
- Close other applications to free RAM
- Consider using smaller models like `ollama pull llama3.2:1b`

## Comparison Test

Try the same code with both models to compare:

1. **With Llama 3.2**: Select "Llama 3.2 (Local)" → Generate
2. **With GPT-OSS**: Select "GPT-OSS 20B (HuggingFace)" → Generate
   - Note: Requires HF_TOKEN environment variable

Compare:
- Generation speed
- Test quality
- Test coverage

## Next Steps

✅ Try different Python functions  
✅ Use **"🔍 Detect Test Smells"** on generated tests  
✅ Compare with Pynguin-generated tests  
✅ Download and run tests locally  

## Need Help?

- 📖 Full documentation: [LLAMA_INTEGRATION.md](LLAMA_INTEGRATION.md)
- 🔧 Configuration guide: [.env.example](.env.example)
- 📝 Integration details: [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)
- 🌐 Ollama docs: https://github.com/ollama/ollama

## System Requirements

| Component | Requirement |
|-----------|-------------|
| RAM | 8GB minimum, 16GB recommended |
| Storage | 5GB for model files |
| CPU | Multi-core processor |
| Internet | Only for initial download |
| OS | Windows 10+, Linux, macOS |

---

**Happy Testing! 🧪**
