
# 🧪 PyTestGenie - Complete Python Testing Pipeline

A comprehensive web application that combines **automated test code generation** and **test smell detection** into one unified platform. Generate quality test code using Pynguin or AI, then analyze it for potential issues.

## 🌟 Features

### Test Code Generator
- **🤖 Pynguin Generation**: Automatic test generation with real-time logs
- **🧠 AI Generation**: Intelligent test creation using OpenAI via HuggingFace
- **📊 Live Streaming**: Watch test generation in real-time
- **💾 Export**: Download generated tests

### Test Smell Detector
- **📝 Code Analysis**: Paste code directly for instant analysis
- **📄 File Upload**: Analyze individual Python test files
- **📁 Directory Upload**: Batch analyze multiple test files
- **🐙 GitHub Integration**: Analyze repositories directly from URL
- **📊 Detailed Reports**: HTML reports with line-by-line smell detection

### Pipeline Integration
Generate tests → Analyze smells → Get detailed reports

## 📁 Project Structure

```
├── backend/                      # Backend API server
│   ├── app_unified.py           # Main Flask application
│   ├── config/                  # Configuration settings
│   │   └── settings.py
│   ├── routes/                  # API route handlers
│   │   ├── test_generation.py  # Test generation endpoints
│   │   └── smell_detection.py  # Smell detection endpoints
│   ├── modules/                 # Core modules
│   │   ├── test_generator/     # Test generation module
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Data models
│   │   │   ├── pynguin_generator.py
│   │   │   └── ai_generator.py
│   │   └── smell_detector/     # Smell detection module
│   │       ├── __init__.py
│   │       ├── analyzer.py     # Main analyzer
│   │       ├── detector.py     # Smell detection logic
│   │       ├── python_parser.py
│   │       ├── components.py
│   │       └── report_generator.py
│   ├── uploads/                 # Temporary file uploads
│   └── report/                  # Generated reports
├── frontend/                    # React frontend
│   └── src/
│       ├── App.jsx             # Main application
│       ├── App.css             # Styles
│       ├── components/
│       │   ├── TestGenerator.jsx
│       │   └── SmellDetector.jsx
│       ├── templates/          # Legacy HTML templates
│       └── static/             # Static assets
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 14+ (for React frontend)
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd TEMPY
```

2. **Create virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy environment template
cp .env.example backend/.env

# Edit backend/.env and add your HuggingFace token
# Get token from: https://huggingface.co/settings/tokens
```

5. **Run the backend**
```bash
cd backend
python app_unified.py
```

Backend will be available at: `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend**
```bash
cd frontend/src
```

2. **Install dependencies**
```bash
npm install axios
```

3. **Run development server**
```bash
# If using Vite
npm run dev

# If using Create React App
npm start
```

Frontend will be available at: `http://localhost:3000` or `http://localhost:5173`

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Test Generation Endpoints

#### Generate Tests (Pynguin)
```http
POST /api/test-generator/generate-tests/pynguin
Content-Type: application/json

{
  "code": "def add(a, b):\n    return a + b"
}

Response: { "task_id": "uuid" }
```

#### Stream Generation Logs
```http
GET /api/test-generator/generate-tests/stream/{task_id}

Server-Sent Events stream
```

#### Generate Tests (AI)
```http
POST /api/test-generator/generate-tests/ai
Content-Type: application/json

{
  "code": "def add(a, b):\n    return a + b"
}

Response: { "test_code": "...", "method": "ai" }
```

### Smell Detection Endpoints

#### Analyze Code
```http
POST /api/smell-detector/analyze/code
Content-Type: application/json

{
  "code": "test code here",
  "filename": "test_example.py"
}

Response: {
  "status": "success",
  "total_smells": 5,
  "smells": [...],
  "report_available": true
}
```

#### Analyze File
```http
POST /api/smell-detector/analyze/file
Content-Type: multipart/form-data

file: <python_file>
```

#### Analyze Directory
```http
POST /api/smell-detector/analyze/directory
Content-Type: multipart/form-data

files[]: <multiple_python_files>
```

#### Analyze GitHub Repository
```http
POST /api/smell-detector/analyze/github
Content-Type: application/json

{
  "github_url": "https://github.com/user/repo"
}
```

#### Get Report
```http
GET /api/smell-detector/report

Returns: HTML report file
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/config/settings.py`:

```python
class Config:
    SECRET_KEY = 'your-secret-key'
    HF_TOKEN = 'your-hf-token'
    CORS_ORIGINS = ['http://localhost:3000']
```

### Frontend Configuration
Edit API_BASE in component files if backend URL changes.

## 🧪 Usage Workflow

### Complete Pipeline Example

1. **Generate Tests**
   - Navigate to "Test Code Generator" tab
   - Choose generation method (Pynguin or AI)
   - Paste your Python code
   - Click "Generate Tests"
   - Wait for generation to complete

2. **Detect Smells**
   - Click "Detect Test Smells" button
   - View analysis results
   - Click "View Full Report" for detailed HTML report

3. **Or Use Smell Detector Directly**
   - Navigate to "Test Smell Detector" tab
   - Choose input method (Code/File/Directory/GitHub)
   - Submit for analysis
   - View results and reports

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt --upgrade
```

**"HuggingFace token not found"**
- Ensure `.env` file exists in `backend/` directory
- Add valid HF_TOKEN to `.env` file

**Pynguin generation fails**
- Ensure code is valid Python
- Check Pynguin logs in console

### Frontend Issues

**CORS errors**
- Verify backend CORS_ORIGINS includes frontend URL
- Restart backend after changing configuration

**"Cannot connect to backend"**
- Ensure backend is running on port 5000
- Check API_BASE URL in component files

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**PyTestGenie** - Making Python testing effortless! 🚀

