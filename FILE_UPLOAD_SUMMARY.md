# File & Project Upload - Implementation Summary

## ✅ Features Implemented

### 1. Three Input Modes
- **Paste Code**: Original manual input (unchanged)
- **Upload File**: Single Python file upload with content preview
- **Upload Project**: Folder upload with module selection

### 2. Backend Endpoints

#### New Routes Added:
1. **`POST /api/test-generator/upload-file`**
   - Accepts single `.py` file
   - Returns file content
   - UTF-8 encoding support

2. **`POST /api/test-generator/upload-project`**
   - Accepts multiple files (folder structure)
   - Stores in temporary directory
   - Returns list of Python files with metadata

3. **`POST /api/test-generator/generate-tests/project`**
   - Generates tests for specific module in uploaded project
   - Uses Pynguin with project-aware mode
   - Supports streaming logs

4. **`GET /api/test-generator/project/{project_id}/file/{filepath}`**
   - Retrieves content of specific file from uploaded project
   - Used for preview when selecting modules

### 3. Frontend Components

#### UI Changes:
- ✅ Input mode selector (radio buttons: Paste/File/Project)
- ✅ File upload button (styled, accepts `.py` only)
- ✅ Project upload button (folder selection with webkitdirectory)
- ✅ Module selector dropdown (lists all Python files in project)
- ✅ Dynamic textarea (read-only for project mode, editable for others)
- ✅ Smart generate button (validates based on input mode)

#### State Management:
```javascript
- inputMode: "paste" | "file" | "project"
- uploadedFile: filename of uploaded file
- projectFiles: array of {path, name, size}
- selectedModule: currently selected module name
- projectId: temporary project identifier
```

### 4. Pynguin Integration

#### New Method:
```python
def generate_tests_for_project(
    project_path: str,
    module_name: str,
    task_queue: queue.Queue,
    algorithm: str = "DYNAMOSA"
)
```

**Features**:
- Project-aware test generation
- Import resolution across modules
- Streaming log support
- Algorithm selection

**Command Generated**:
```bash
pynguin \
  --project-path <uploaded_project_path> \
  --module-name <selected_module> \
  --output-path <temp_output> \
  --algorithm <selected_algorithm>
```

---

## 📁 Files Modified

### Backend:
1. **`backend/routes/test_generation.py`**
   - Added `allowed_file()` helper
   - Added 4 new endpoints
   - Import additions: `tempfile`, `shutil`, `Path`, `secure_filename`

2. **`backend/modules/test_generator/pynguin_generator.py`**
   - Added `generate_tests_for_project()` method
   - Project-aware Pynguin execution
   - Enhanced error handling

### Frontend:
3. **`frontend/src/components/TestGenerator.jsx`**
   - Added 5 new state variables
   - Added `handleFileUpload()` function
   - Added `handleProjectUpload()` function
   - Added `handleModuleSelect()` function
   - Updated `handleGenerate()` with multi-mode support
   - Added UI components for file/project selection

---

## 🎯 How It Works

### Flow 1: Upload File Mode
```
User clicks "Upload File"
  ↓
Selects .py file
  ↓
POST /upload-file (FormData)
  ↓
Backend reads file content
  ↓
Returns {filename, content, size}
  ↓
Frontend sets code state
  ↓
User clicks "Generate Tests"
  ↓
Uses existing AI/Pynguin flow
```

### Flow 2: Upload Project Mode (Pynguin)
```
User clicks "Upload Project"
  ↓
Selects folder (multiple files)
  ↓
POST /upload-project (FormData with webkitRelativePath)
  ↓
Backend stores in temp directory
  ↓
Returns {project_id, files[]}
  ↓
Frontend shows module dropdown
  ↓
User selects module
  ↓
GET /project/{id}/file/{path} (preview)
  ↓
User clicks "Generate Tests"
  ↓
POST /generate-tests/project {project_id, module_name, algorithm}
  ↓
Backend runs Pynguin on project
  ↓
Streams logs → Frontend displays
  ↓
Returns generated tests
```

### Flow 3: Upload Project Mode (AI)
```
User uploads project
  ↓
Selects module
  ↓
File content loads into textarea
  ↓
User clicks "Generate Tests"
  ↓
POST /generate-tests/ai {code, model}
  ↓
AI generates tests for that module only
```

---

## 🔒 Security Features

1. **File Validation**:
   - Only `.py` files accepted
   - Extension check: `Path(filename).suffix in ALLOWED_EXTENSIONS`

2. **Filename Sanitization**:
   - Uses `secure_filename()` from werkzeug
   - Prevents path traversal attacks

3. **Temporary Storage**:
   - Projects stored in `tempfile.mkdtemp()`
   - Unique project IDs (directory basename)
   - Isolated storage per upload

4. **Size Limits**:
   - Configured in Flask: `MAX_CONTENT_LENGTH = 16MB`

---

## 💡 Use Cases

### Use Case 1: Single Function
**Input Mode**: Paste or Upload File
**Method**: AI or Pynguin
**Best For**: Quick tests, learning, small utilities

### Use Case 2: Standalone Module
**Input Mode**: Upload File
**Method**: Pynguin or AI
**Best For**: Single-file projects, scripts

### Use Case 3: Multi-Module Project
**Input Mode**: Upload Project
**Method**: Pynguin (recommended)
**Best For**: Projects with dependencies, packages, complex structures

**Example**:
```
myproject/
├── calculator.py (imports utils)
├── utils.py
└── validators.py
```
Select `calculator` → Pynguin resolves imports from `utils.py`

---

## 🧪 Testing

### Test File Upload
```bash
curl -X POST http://localhost:5000/api/test-generator/upload-file \
  -F "file=@calculator.py"
```

### Test Project Upload
```bash
# Create test project
mkdir test_project
echo "def add(a,b): return a+b" > test_project/calc.py
echo "def validate(n): return isinstance(n, int)" > test_project/utils.py

# Upload (use form-data in Postman or similar tool)
# Browser automatically handles webkitdirectory
```

### Test Project Generation
```bash
curl -X POST http://localhost:5000/api/test-generator/generate-tests/project \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "pytestgenie_project_abc123",
    "module_name": "calc",
    "algorithm": "DYNAMOSA"
  }'
```

---

## 📊 Comparison: Before vs After

| Feature | Before | After |
|---------|--------|-------|
| Input methods | 1 (paste only) | 3 (paste, file, project) |
| File support | ❌ | ✅ |
| Project support | ❌ | ✅ |
| Import resolution | Limited | ✅ Full (project mode) |
| Module selection | N/A | ✅ Dropdown |
| Pynguin project mode | ❌ | ✅ |
| Multi-file testing | ❌ | ✅ |

---

## 🚀 Quick Start

### Upload a File:
1. Open PyTestGenie
2. Select **"Upload File"** input mode
3. Click **"📄 Choose Python File"**
4. Select your `.py` file
5. Choose generation method (AI/Pynguin)
6. Click **"🚀 Generate Tests"**

### Upload a Project:
1. Select **"Upload Project"** input mode
2. Click **"📁 Choose Project Folder"**
3. Select your project folder
4. Choose a module from the dropdown
5. Select Pynguin (recommended)
6. Click **"🚀 Generate Tests"**

---

## 🐛 Known Limitations

1. **Folder Upload Browser Support**:
   - Uses `webkitdirectory` (widely supported)
   - May not work in very old browsers

2. **Project Size**:
   - Limited by `MAX_CONTENT_LENGTH` (default 16MB)
   - Very large projects may timeout

3. **Temporary Storage**:
   - Projects not persisted between sessions
   - Need to re-upload if page refreshed

4. **AI Project Mode**:
   - Tests only selected module (no project context)
   - For project-aware testing, use Pynguin

---

## 🔮 Future Improvements

Possible enhancements:
- [ ] Project persistence (save between sessions)
- [ ] Batch testing (multiple modules at once)
- [ ] ZIP file upload support
- [ ] Git repository URL input
- [ ] Project caching
- [ ] Progress bars for uploads
- [ ] File tree visualization
- [ ] Drag & drop upload

---

## 📖 Documentation

- **Full Guide**: [FILE_UPLOAD_GUIDE.md](FILE_UPLOAD_GUIDE.md)
- **API Docs**: See backend route docstrings
- **Examples**: See guide for detailed use cases

---

## ✨ Summary

The file and project upload feature significantly enhances PyTestGenie's capabilities:

✅ **Flexibility**: 3 input modes to suit different needs
✅ **Project-Aware**: Pynguin can resolve imports and dependencies
✅ **User-Friendly**: Intuitive UI with clear visual feedback
✅ **Secure**: Proper validation and sandboxing
✅ **Compatible**: Works with both Pynguin and AI methods

All existing functionality preserved - paste code still works exactly as before!

---

**Ready to use!** 🎉

Start by restarting your backend and frontend servers, then try uploading a Python file or project to see it in action.
