# 🚀 Quick Reference: File & Project Upload

## Input Modes at a Glance

| Mode | Icon | When to Use | Supports |
|------|------|-------------|----------|
| **Paste Code** | 📝 | Quick tests, learning | AI ✅ Pynguin ✅ |
| **Upload File** | 📄 | Single module | AI ✅ Pynguin ✅ |
| **Upload Project** | 📁 | Multi-file projects | AI ✅ Pynguin ✅* |

\* *Pynguin recommended for project mode (import resolution)*

---

## Quick Actions

### Upload a Single File
```
1. Click "Upload File" mode
2. Click "📄 Choose Python File"
3. Select .py file
4. Generate!
```

### Upload a Project
```
1. Click "Upload Project" mode
2. Click "📁 Choose Project Folder"
3. Select folder
4. Choose module from dropdown
5. Generate!
```

---

## API Quick Reference

### Upload File
```bash
curl -X POST http://localhost:5000/api/test-generator/upload-file \
  -F "file=@myfile.py"
```

### Upload Project
```javascript
const formData = new FormData();
for (let file of files) {
  formData.append('files', file, file.webkitRelativePath);
}
axios.post('/upload-project', formData);
```

### Generate for Project
```bash
curl -X POST http://localhost:5000/api/test-generator/generate-tests/project \
  -H "Content-Type: application/json" \
  -d '{"project_id":"xyz", "module_name":"calculator", "algorithm":"DYNAMOSA"}'
```

---

## Examples

### Example 1: Test a Utility Function
```python
# utils.py
def format_currency(amount):
    return f"${amount:,.2f}"
```
**Action**: Upload File → AI/Pynguin → Generate

---

### Example 2: Test Project with Dependencies
```
myproject/
├── calculator.py    # imports from utils
└── utils.py
```
**Action**: Upload Project → Select `calculator` → Pynguin → Generate

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No file provided" | Select a file first |
| "Only .py files allowed" | Check file extension |
| "Invalid project_id" | Re-upload project |
| No files in dropdown | Check folder has .py files |

---

## Tips

💡 **For single files**: Use Upload File or Paste  
💡 **For projects**: Use Upload Project + Pynguin  
💡 **For quick tests**: Use Paste Code + AI  
💡 **For imports**: Use Upload Project mode  

---

## Status Indicators

- ✅ **Green checkmark**: File uploaded successfully
- 📁 **File list**: Project uploaded, select module
- 🔒 **Read-only textarea**: Project mode (view only)
- ⏳ **Generating...**: Test generation in progress

---

## Keyboard Shortcuts

- `Ctrl/Cmd + Click` file button: Opens file selector
- Select folder: Hold and select folder (browser-specific)

---

## File Size Limits

- Maximum file size: **16 MB** (configurable)
- Maximum project size: **16 MB total** (configurable)
- Supported extension: **.py only**

---

## Need More Help?

- 📖 **Full Guide**: [FILE_UPLOAD_GUIDE.md](FILE_UPLOAD_GUIDE.md)
- 📋 **Summary**: [FILE_UPLOAD_SUMMARY.md](FILE_UPLOAD_SUMMARY.md)
- 🤖 **Llama Integration**: [LLAMA_INTEGRATION.md](LLAMA_INTEGRATION.md)

---

**Happy Testing!** 🎉
