# File & Project Upload Guide

## Overview

PyTestGenie now supports **three input modes** for test generation:

1. **📝 Paste Code** - Manually paste code snippets (original method)
2. **📄 Upload File** - Upload a single Python file
3. **📁 Upload Project** - Upload an entire project folder and select specific modules

This flexibility allows you to generate tests for both standalone code snippets and complex multi-file projects.

---

## Input Modes

### 1. Paste Code (Default)
**Best for**: Quick testing, small functions, learning

**How to use**:
1. Select "Paste Code" input mode
2. Paste your Python code in the textarea
3. Choose generation method (Pynguin or AI)
4. Click "Generate Tests"

**Example**:
```python
def calculate_sum(numbers):
    return sum(numbers)

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0
```

---

### 2. Upload File
**Best for**: Single module testing, standalone files

**How to use**:
1. Select "Upload File" input mode
2. Click "📄 Choose Python File" button
3. Select a `.py` file from your computer
4. The file content will automatically load into the textarea
5. Choose generation method (Pynguin or AI)
6. Click "Generate Tests"

**Supported**:
- ✅ `.py` files only
- ✅ UTF-8 encoded files
- ✅ Files up to 16MB (configurable)

**Features**:
- File content is displayed for review
- You can edit the loaded code before generation
- Supports both AI and Pynguin methods

---

### 3. Upload Project
**Best for**: Multi-module projects, complex codebases

**How to use**:
1. Select "Upload Project" input mode
2. Click "📁 Choose Project Folder" button
3. Select your entire project folder
4. All Python files will be listed in a dropdown
5. Select the module you want to test
6. The selected module's code will load (read-only preview)
7. Choose generation method:
   - **Pynguin**: Project-based generation (recommended)
   - **AI**: Generates tests for the selected module only
8. Click "Generate Tests"

**Project Structure Example**:
```
my_project/
├── calculator.py
├── utils.py
├── models/
│   ├── __init__.py
│   └── user.py
└── services/
    ├── __init__.py
    └── auth.py
```

**Features**:
- ✅ Preserves folder structure
- ✅ Lists all `.py` files with file sizes
- ✅ Shows module paths (e.g., `models/user.py`)
- ✅ Supports nested directories
- ✅ Project-aware Pynguin generation

---

## Generation Methods

### Pynguin (Automatic)

#### For Paste/Upload File:
```bash
pynguin \
  --project-path <temp_directory> \
  --module-name user_code \
  --output-path <output_directory> \
  --algorithm DYNAMOSA
```

#### For Upload Project:
```bash
pynguin \
  --project-path <your_project_path> \
  --module-name <selected_module> \
  --output-path <output_directory> \
  --algorithm DYNAMOSA
```

**Benefits**:
- Project-aware (can resolve imports between modules)
- Supports all Pynguin algorithms
- Streaming logs for progress tracking

### AI (GPT-OSS / Llama 3.2)

For all input modes:
- Analyzes the code content
- Generates pytest tests using AI
- Works with both cloud (GPT-OSS) and local (Llama 3.2) models

---

## API Endpoints

### 1. Upload Single File
```http
POST /api/test-generator/upload-file
Content-Type: multipart/form-data

file: <Python file>
```

**Response**:
```json
{
  "filename": "calculator.py",
  "content": "def add(a, b):\n    return a + b",
  "size": 45
}
```

### 2. Upload Project
```http
POST /api/test-generator/upload-project
Content-Type: multipart/form-data

files: <Multiple Python files with paths>
```

**Response**:
```json
{
  "project_id": "pytestgenie_project_abc123",
  "files": [
    {"path": "calculator.py", "name": "calculator.py", "size": 1024},
    {"path": "utils.py", "name": "utils.py", "size": 2048}
  ],
  "total_files": 2
}
```

### 3. Generate Tests for Project Module
```http
POST /api/test-generator/generate-tests/project
Content-Type: application/json

{
  "project_id": "pytestgenie_project_abc123",
  "module_name": "calculator",
  "algorithm": "DYNAMOSA"
}
```

**Response**:
```json
{
  "task_id": "uuid-task-id"
}
```

Then stream results from:
```http
GET /api/test-generator/generate-tests/stream/{task_id}
```

### 4. Get Project File Content
```http
GET /api/test-generator/project/{project_id}/file/{filepath}
```

**Response**:
```json
{
  "filepath": "calculator.py",
  "content": "def add(a, b):\n    return a + b",
  "size": 45
}
```

---

## Use Cases

### Use Case 1: Single Function Testing
**Scenario**: Test a simple utility function

**Method**: Paste Code or Upload File

**Steps**:
1. Create `utils.py`:
```python
def format_phone(number):
    """Format phone number to (XXX) XXX-XXXX"""
    digits = ''.join(c for c in number if c.isdigit())
    if len(digits) != 10:
        raise ValueError("Phone number must be 10 digits")
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
```
2. Upload file or paste code
3. Select AI or Pynguin
4. Generate tests

---

### Use Case 2: Multi-Module Project
**Scenario**: Test a calculator module that imports from utils

**Project Structure**:
```
calculator_project/
├── calculator.py
└── utils.py
```

**calculator.py**:
```python
from utils import validate_number

def add(a, b):
    validate_number(a)
    validate_number(b)
    return a + b
```

**utils.py**:
```python
def validate_number(n):
    if not isinstance(n, (int, float)):
        raise TypeError("Must be a number")
```

**Steps**:
1. Select "Upload Project"
2. Choose the `calculator_project` folder
3. Select `calculator` module from dropdown
4. Choose Pynguin (recommended for project-aware testing)
5. Generate tests

**Benefits**:
- Pynguin can resolve the `from utils import validate_number`
- Tests will consider the dependency between modules
- More accurate test generation

---

### Use Case 3: Testing a Class in a Package
**Scenario**: Test a User model in a models package

**Project Structure**:
```
myapp/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── user.py
└── utils/
    ├── __init__.py
    └── validators.py
```

**Steps**:
1. Upload entire `myapp` folder
2. Select `models/user` from dropdown
3. Generate tests with Pynguin

---

## Frontend Components

### Input Mode Selector
```jsx
<div className="input-mode-selector">
  <label>📥 Input Mode:</label>
  <label className="radio-label">
    <input type="radio" value="paste" />
    <span>Paste Code</span>
  </label>
  <label className="radio-label">
    <input type="radio" value="file" />
    <span>Upload File</span>
  </label>
  <label className="radio-label">
    <input type="radio" value="project" />
    <span>Upload Project</span>
  </label>
</div>
```

### File Upload Button
```jsx
<label htmlFor="file-upload">
  📄 Choose Python File
</label>
<input 
  id="file-upload" 
  type="file" 
  accept=".py"
  onChange={handleFileUpload}
/>
```

### Project Upload with Module Selector
```jsx
<label htmlFor="project-upload">
  📁 Choose Project Folder
</label>
<input 
  id="project-upload" 
  type="file" 
  webkitdirectory="true"
  multiple
  onChange={handleProjectUpload}
/>

{projectFiles.length > 0 && (
  <select onChange={handleModuleSelect}>
    <option value="">-- Select a module --</option>
    {projectFiles.map(file => (
      <option value={file.path}>
        {file.path} ({file.size} KB)
      </option>
    ))}
  </select>
)}
```

---

## Configuration

### Backend Settings
```python
# config/settings.py
class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### Allowed Extensions
```python
# routes/test_generation.py
ALLOWED_EXTENSIONS = {'.py'}

def allowed_file(filename):
    return Path(filename).suffix in ALLOWED_EXTENSIONS
```

---

## Security Considerations

✅ **File Validation**:
- Only `.py` files accepted
- Secure filename sanitization
- File size limits enforced

✅ **Temporary Storage**:
- Projects stored in temporary directories
- Auto-cleanup after processing
- Unique project IDs prevent conflicts

✅ **Path Traversal Prevention**:
- All paths are validated
- Relative paths handled safely
- No access outside project directory

---

## Error Handling

### Common Errors

**Error**: "No file provided"
- **Cause**: File input is empty
- **Solution**: Select a file before uploading

**Error**: "Only .py files are allowed"
- **Cause**: Uploaded non-Python file
- **Solution**: Select a `.py` file

**Error**: "Invalid project_id"
- **Cause**: Project session expired or invalid ID
- **Solution**: Re-upload the project

**Error**: "Module not found"
- **Cause**: Selected module doesn't exist in project
- **Solution**: Verify the module name and file structure

---

## Tips & Best Practices

### 1. Choosing Input Mode
| Input Mode | When to Use |
|------------|-------------|
| **Paste Code** | Learning, quick tests, simple functions |
| **Upload File** | Single module, standalone scripts |
| **Upload Project** | Multi-file projects, complex dependencies |

### 2. Pynguin vs AI
| Method | Best For | Project Upload |
|--------|----------|----------------|
| **Pynguin** | Automatic coverage, large projects | ✅ Recommended |
| **AI** | Readable tests, business logic | ✅ Supported (single module) |

### 3. Project Organization
- Keep projects well-structured
- Use meaningful module names
- Avoid circular dependencies
- Include `__init__.py` in packages

### 4. Performance
- Large projects: Use Pynguin project mode
- Single functions: Paste or upload file
- Complex logic: Try AI models

---

## Examples

### Example 1: Upload and Test Calculator File

**File**: `calculator.py`
```python
class Calculator:
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

**Steps**:
1. Click "Upload File"
2. Select `calculator.py`
3. Choose AI (Llama 3.2)
4. Generate tests

**Result**: Comprehensive pytest tests with edge cases

---

### Example 2: Project-Based Testing

**Project**: E-commerce System
```
ecommerce/
├── models/
│   ├── __init__.py
│   ├── product.py
│   └── order.py
├── services/
│   ├── __init__.py
│   ├── cart.py
│   └── payment.py
└── utils/
    ├── __init__.py
    └── validators.py
```

**Target**: Test `services/cart.py` (which imports from models)

**Steps**:
1. Upload entire `ecommerce` folder
2. Select `services/cart` from dropdown
3. Choose Pynguin (DYNAMOSA)
4. Generate tests

**Benefits**:
- Pynguin resolves imports from `models`
- Tests consider relationships between modules
- Coverage analysis across dependencies

---

## Troubleshooting

### Issue: File Upload Button Not Working
**Solution**:
- Check file permissions
- Verify file size (< 16MB)
- Ensure `.py` extension

### Issue: Project Upload Shows No Files
**Solution**:
- Verify folder contains `.py` files
- Check browser console for errors
- Try uploading a smaller project first

### Issue: Module Selection Empty
**Solution**:
- Ensure project uploaded successfully
- Check that Python files have `.py` extension
- Refresh and try again

### Issue: Pynguin Fails with "Module Not Found"
**Solution**:
- Verify module name matches filename
- Check for typos in module name
- Ensure file is in project root or proper package

---

## Future Enhancements

Planned features:
- 📦 Support for requirements.txt upload
- 🔄 Batch testing (multiple modules at once)
- 💾 Project history and caching
- 📊 Test coverage visualization
- 🎯 Selective file upload (choose specific files)
- 🔗 Git repository integration

---

## Summary

The file and project upload feature provides flexible input options:
- **Quick**: Paste code for instant testing
- **Simple**: Upload single files
- **Advanced**: Upload projects for comprehensive testing

All three modes work seamlessly with both Pynguin and AI test generation, giving you complete flexibility in how you generate tests!
