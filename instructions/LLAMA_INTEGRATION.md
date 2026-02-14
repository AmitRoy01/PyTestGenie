# Llama 3.2 Integration Guide

## Overview
PyTestGenie now supports multiple AI models for test generation:
- **GPT-OSS 20B** (via HuggingFace) - Cloud-based model
- **Llama 3.2** (Local) - Locally hosted model via Ollama

## Prerequisites

### For Llama 3.2 (Local)
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull Llama 3.2 model**:
   ```bash
   ollama pull llama3.2
   ```
3. **Start Ollama server** (usually starts automatically):
   ```bash
   ollama serve
   ```
   Default URL: `http://localhost:11434`

### For GPT-OSS (HuggingFace)
1. Get a HuggingFace token from [huggingface.co](https://huggingface.co/settings/tokens)
2. Set environment variable:
   ```bash
   # Windows
   set HF_TOKEN=your_token_here
   
   # Linux/Mac
   export HF_TOKEN=your_token_here
   ```

## Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# HuggingFace token (required for GPT-OSS)
HF_TOKEN=your_huggingface_token

# Llama API URL (optional, defaults to localhost:11434)
LLAMA_API_URL=http://localhost:11434/v1
```

### Custom Llama Server URL
If your Llama server runs on a different port or host:
```env
LLAMA_API_URL=http://192.168.1.100:11434/v1
```

## Usage

### Web Interface
1. Navigate to the Test Generator module
2. Select **"🧠 AI (OpenAI/HuggingFace)"** option
3. From the **"🤖 AI Model"** dropdown, choose:
   - **GPT-OSS 20B (HuggingFace)** - for cloud-based generation
   - **Llama 3.2 (Local)** - for local generation
4. Paste your Python code
5. Click **"🚀 Generate Tests"**

### API Usage

#### Generate tests with GPT-OSS:
```bash
curl -X POST http://localhost:5000/api/test-generator/generate-tests/ai \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "model": "gpt-oss"
  }'
```

#### Generate tests with Llama 3.2:
```bash
curl -X POST http://localhost:5000/api/test-generator/generate-tests/ai \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "model": "llama-3.2"
  }'
```

## How It Works

### Model Configuration
The `AITestGenerator` class supports multiple models through a configuration dictionary:

```python
MODELS = {
    "gpt-oss": {
        "name": "GPT-OSS 20B",
        "model_id": "openai/gpt-oss-20b:groq",
        "base_url": "https://router.huggingface.co/v1",
        "requires_hf_token": True
    },
    "llama-3.2": {
        "name": "Llama 3.2",
        "model_id": "llama3.2",
        "base_url": "http://localhost:11434/v1",
        "requires_hf_token": False
    }
}
```

### Code Flow
1. User selects AI model in frontend
2. Frontend sends request with `model` parameter
3. Backend creates `AITestGenerator` with specified model
4. Generator configures OpenAI client with appropriate base URL and API key
5. Tests are generated using the selected model
6. Response includes generated test code and model used

## Troubleshooting

### Llama 3.2 Connection Issues
**Error**: "Connection refused" or "Failed to connect to Llama server"

**Solutions**:
1. Verify Ollama is running:
   ```bash
   ollama list
   ```
2. Check if model is available:
   ```bash
   ollama run llama3.2 "Hello"
   ```
3. Test API endpoint:
   ```bash
   curl http://localhost:11434/api/tags
   ```
4. Verify firewall isn't blocking port 11434

### GPT-OSS Token Issues
**Error**: "HuggingFace token not found"

**Solutions**:
1. Verify token is set:
   ```bash
   # Windows
   echo %HF_TOKEN%
   
   # Linux/Mac
   echo $HF_TOKEN
   ```
2. Restart your terminal/IDE after setting environment variable
3. Check token validity at [huggingface.co](https://huggingface.co/settings/tokens)

### Model Not Found
**Error**: "Unsupported model"

**Solutions**:
1. Check available models in `ai_generator.py` MODELS dictionary
2. Ensure model name matches exactly: `gpt-oss` or `llama-3.2`
3. Verify spelling in API request

## Adding New Models

To add support for additional models:

1. **Edit `ai_generator.py`**:
```python
MODELS = {
    # ... existing models ...
    "your-model": {
        "name": "Your Model Name",
        "model_id": "model_identifier",
        "base_url": "http://your-api-url",
        "requires_hf_token": False
    }
}
```

2. **Update `TestGenerator.jsx`**:
```jsx
<select id="model-select" value={aiModel} onChange={(e) => setAiModel(e.target.value)}>
  <option value="gpt-oss">GPT-OSS 20B (HuggingFace)</option>
  <option value="llama-3.2">Llama 3.2 (Local)</option>
  <option value="your-model">Your Model Name</option>
</select>
```

## Performance Comparison

| Model | Speed | Quality | Cost | Requirements |
|-------|-------|---------|------|--------------|
| GPT-OSS 20B | Fast | High | API calls | HF Token, Internet |
| Llama 3.2 | Medium | High | Free | Local compute, 8GB+ RAM |

## Benefits of Local Llama 3.2
✅ **Privacy**: Code stays on your machine  
✅ **Cost**: No API charges  
✅ **Offline**: Works without internet  
✅ **Control**: Full control over model parameters  

## System Requirements for Llama 3.2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: ~5GB for model files
- **OS**: Windows, Linux, or macOS
- **CPU**: Modern multi-core processor (or GPU for faster inference)

## Next Steps
- Try both models to compare results
- Fine-tune Llama 3.2 for your specific testing needs
- Experiment with different algorithms in Pynguin mode
- Combine AI-generated tests with test smell detection

For more information, see:
- [Ollama Documentation](https://github.com/ollama/ollama)
- [HuggingFace Documentation](https://huggingface.co/docs)
- [Project README](README.md)
