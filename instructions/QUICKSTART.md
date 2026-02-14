# 🚀 PyTestGenie - Quick Start Guide

## Installation (5 minutes)

### Step 1: Setup Backend
```bash
# Navigate to project
cd TEMPY

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Create .env file in backend folder
cd backend
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env and add your HuggingFace token
# Get token from: https://huggingface.co/settings/tokens
```

### Step 3: Setup Frontend
```bash
cd ../frontend
npm install
```

## Running the Application

### Option 1: Use Startup Scripts

**Windows:**
```bash
# From project root
run_backend.bat
```

**Linux/Mac:**
```bash
chmod +x run_backend.sh
./run_backend.sh
```

Then in another terminal:
```bash
cd frontend
npm run dev
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python app_unified.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Docs**: http://localhost:5000/

## First Usage

### Generate Test Code

1. Open http://localhost:3000
2. Click **"Test Code Generator"** tab
3. Choose method:
   - **Pynguin**: Automatic generation with logs
   - **AI**: Intelligent generation (requires HF token)
4. Paste your Python code
5. Click **"Generate Tests"**
6. Wait for results
7. Download or analyze for smells

### Detect Test Smells

1. Click **"Test Smell Detector"** tab
2. Choose input method:
   - **Code**: Paste code directly
   - **File**: Upload .py file
   - **Directory**: Upload multiple files
   - **GitHub**: Enter repository URL
3. Click **"Analyze"**
4. View results and detailed report

### Complete Pipeline

1. Generate tests (Test Generator)
2. Click **"Detect Test Smells"** on generated code
3. View detailed HTML report
4. Download clean test code

## Verification

Check if everything works:

```bash
# Backend health check
curl http://localhost:5000/health

# Expected response: {"status": "healthy"}
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 14+

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "HuggingFace token not found"
1. Create backend/.env file
2. Add: `HF_TOKEN=your_token_here`
3. Get token from: https://huggingface.co/settings/tokens

### CORS errors
1. Check backend is running on port 5000
2. Verify CORS_ORIGINS in backend/.env includes frontend URL
3. Restart backend after changes

## Example Code to Test

### Simple Function
```python
def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b
```

### Class Example
```python
class Calculator:
    """Simple calculator class."""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

## Next Steps

1. ✅ Generate test code for your projects
2. ✅ Analyze existing test files for smells
3. ✅ Review generated HTML reports
4. ✅ Integrate into your workflow
5. ✅ Read ARCHITECTURE.md for details

## Need Help?

- 📚 Read README.md for full documentation
- 🏗️ Check ARCHITECTURE.md for technical details
- 🐛 Report issues on GitHub
- 💬 Check existing issues for solutions

## Tips

- **Pynguin**: Best for simple functions, provides detailed logs
- **AI**: Better for complex code, faster but requires API token
- **Pipeline**: Generate → Analyze → Fix → Deploy
- **Reports**: HTML reports are saved in backend/report/
- **Downloads**: Generated tests saved as test_generated.py

Happy Testing! 🧪✨
