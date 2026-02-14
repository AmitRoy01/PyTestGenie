# Visual Guide: File & Project Upload

## UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    📝 Generate Test Code                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Method:  ○ 🤖 Pynguin (Automatic)  ● 🧠 AI (OpenAI/HF)       │
│                                                                 │
│  📥 Input Mode:                                                 │
│     ○ Paste Code    ● Upload File    ○ Upload Project          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  📄 Choose Python File                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ✓ calculator.py                                                │
│                                                                 │
│  🤖 AI Model:  [Llama 3.2 (Local) ▼]                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  def add(a, b):                                         │   │
│  │      return a + b                                       │   │
│  │                                                         │   │
│  │  def multiply(a, b):                                    │   │
│  │      return a * b                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           🚀 Generate Tests                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mode Comparisons

### Mode 1: Paste Code (Default)
```
┌────────────────────────────────────────┐
│  Input Mode:                           │
│  ● Paste Code                          │
│  ○ Upload File                         │
│  ○ Upload Project                      │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  Textarea (editable)                   │
│  > User types or pastes code           │
│  > Direct editing enabled              │
└────────────────────────────────────────┘
         ↓
    Generate Tests
```

### Mode 2: Upload File
```
┌────────────────────────────────────────┐
│  Input Mode:                           │
│  ○ Paste Code                          │
│  ● Upload File                         │
│  ○ Upload Project                      │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  📄 Choose Python File  [Button]       │
│  ✓ myfile.py                           │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  Textarea (editable)                   │
│  > File content loaded                 │
│  > Can be modified before generation   │
└────────────────────────────────────────┘
         ↓
    Generate Tests
```

### Mode 3: Upload Project
```
┌────────────────────────────────────────┐
│  Input Mode:                           │
│  ○ Paste Code                          │
│  ○ Upload File                         │
│  ● Upload Project                      │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  📁 Choose Project Folder  [Button]    │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  Select Module to Test:                │
│  [-- Select a module -- ▼]             │
│  Options:                              │
│    calculator.py (2.5 KB)              │
│    utils.py (1.2 KB)                   │
│    models/user.py (3.8 KB)             │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│  Textarea (read-only, preview)         │
│  > Selected module content shown       │
│  > Cannot be edited (project context)  │
└────────────────────────────────────────┘
         ↓
    Generate Tests (Project-Aware)
```

---

## Step-by-Step Flows

### Flow A: Upload Single File → AI Generation

```
   Start
     │
     ├─ 1. Select "Upload File" mode
     │
     ├─ 2. Click "📄 Choose Python File"
     │         │
     │         ├─ File picker opens
     │         │
     │         └─ Select calculator.py
     │
     ├─ 3. File uploads
     │         │
     │         ├─ Shows: "✓ calculator.py"
     │         │
     │         └─ Content loads in textarea
     │
     ├─ 4. Select AI method
     │         │
     │         └─ Choose model: Llama 3.2
     │
     ├─ 5. Click "🚀 Generate Tests"
     │         │
     │         ├─ Button shows: "⏳ Generating..."
     │         │
     │         └─ AI processes code
     │
     └─ 6. View Results
               │
               ├─ Generated test code appears
               │
               └─ Options: Download, Detect Smells
```

### Flow B: Upload Project → Pynguin Generation

```
   Start
     │
     ├─ 1. Select "Upload Project" mode
     │
     ├─ 2. Click "📁 Choose Project Folder"
     │         │
     │         ├─ Folder picker opens
     │         │
     │         └─ Select project folder
     │
     ├─ 3. Project uploads
     │         │
     │         ├─ All .py files detected
     │         │
     │         └─ Dropdown populated with modules
     │
     ├─ 4. Select module from dropdown
     │         │
     │         ├─ Choose: calculator
     │         │
     │         └─ File content previews (read-only)
     │
     ├─ 5. Keep Pynguin method selected
     │         │
     │         └─ Algorithm: DYNAMOSA (default)
     │
     ├─ 6. Click "🚀 Generate Tests"
     │         │
     │         ├─ Pynguin runs on project
     │         │
     │         ├─ Resolves imports from other files
     │         │
     │         └─ Logs stream in real-time
     │
     └─ 7. View Results
               │
               ├─ Generated test code appears
               │
               ├─ Tests include project context
               │
               └─ Options: Download, Detect Smells
```

---

## Project Structure Examples

### Example 1: Simple Project

```
my_calculator/
├── calculator.py    ← Select this module
└── utils.py         ← Imported by calculator.py

After upload:
┌─────────────────────────────────┐
│ Select Module to Test:          │
│ [calculator ▼]                   │
│                                  │
│ Dropdown options:                │
│  ⚬ calculator                    │
│  ⚬ utils                         │
└─────────────────────────────────┘
```

### Example 2: Package Structure

```
myproject/
├── __init__.py
├── calculator.py
├── models/
│   ├── __init__.py
│   └── user.py      ← Select this module
└── services/
    ├── __init__.py
    └── auth.py

After upload:
┌─────────────────────────────────┐
│ Select Module to Test:          │
│ [models/user ▼]                  │
│                                  │
│ Dropdown options:                │
│  ⚬ calculator                    │
│  ⚬ models/user                   │
│  ⚬ services/auth                 │
└─────────────────────────────────┘
```

---

## Visual State Indicators

### File Upload States

```
Initial State:
┌────────────────────────────────┐
│ 📄 Choose Python File          │
└────────────────────────────────┘

After Upload:
┌────────────────────────────────┐
│ 📄 Choose Python File          │
└────────────────────────────────┘
  ✓ calculator.py    ← Green checkmark
```

### Project Upload States

```
Initial State:
┌────────────────────────────────┐
│ 📁 Choose Project Folder       │
└────────────────────────────────┘
┌────────────────────────────────┐
│ Select Module to Test:         │
│ [-- Select a module -- ▼]      │  ← Disabled
└────────────────────────────────┘

After Upload:
┌────────────────────────────────┐
│ 📁 Choose Project Folder       │
└────────────────────────────────┘
✓ Project uploaded! Found 3 Python files.

┌────────────────────────────────┐
│ Select Module to Test:         │
│ [-- Select a module -- ▼]      │  ← Enabled
│                                │
│  calculator.py (2.5 KB)        │
│  utils.py (1.2 KB)             │
│  models/user.py (3.8 KB)       │
└────────────────────────────────┘
```

### Generation States

```
Ready:
┌────────────────────────────────┐
│   🚀 Generate Tests            │  ← Blue, enabled
└────────────────────────────────┘

Loading:
┌────────────────────────────────┐
│   ⏳ Generating...             │  ← Gray, disabled
└────────────────────────────────┘

Complete:
┌────────────────────────────────┐
│   🚀 Generate Tests            │  ← Blue, enabled again
└────────────────────────────────┘
```

---

## Input Mode Decision Tree

```
                 Need to test code?
                        │
           ┌────────────┼────────────┐
           │            │            │
      Simple code?  Single file?  Project with
      Small snippet?  No deps?    multiple files?
           │            │            │
           ↓            ↓            ↓
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  PASTE   │  │   FILE   │  │ PROJECT  │
    │   CODE   │  │  UPLOAD  │  │  UPLOAD  │
    └──────────┘  └──────────┘  └──────────┘
         │            │            │
         ↓            ↓            ↓
    Quick test    Standalone    Full project
    Learning      module        context
    Prototyping   Script        Import resolution
```

---

## Color Coding (Conceptual)

```
🟢 Green: Success, uploaded, valid
🔵 Blue: Action buttons, primary
🟡 Yellow: Warning, attention
🔴 Red: Error, invalid
⚪ Gray: Disabled, inactive
```

---

## File Type Icons

```
📄 .py file
📁 Folder/Project
📝 Text/Code
🤖 Pynguin
🧠 AI
🔧 Algorithm
⚙️ Settings
✅ Success
❌ Error
⏳ Loading
```

---

## Responsive Layout (Conceptual)

```
Desktop View:
┌─────────────────────────────────────┐
│  [All controls in single column]   │
│  [Wide textarea]                    │
│  [Full-width button]                │
└─────────────────────────────────────┘

Mobile View (Stacked):
┌─────────────┐
│  Controls   │
│  (stacked)  │
├─────────────┤
│  Textarea   │
│  (narrow)   │
├─────────────┤
│   Button    │
└─────────────┘
```

---

## Summary Diagram

```
                PyTestGenie Test Generator
                           │
            ┌──────────────┼──────────────┐
            │              │              │
       Input Mode:    Input Mode:    Input Mode:
        Paste Code    Upload File    Upload Project
            │              │              │
            │              ↓              │
            │         File Upload         │
            │         (single .py)        │
            │              │              ↓
            │              │         Folder Upload
            │              │         (multiple .py)
            │              │              │
            │              │              ↓
            │              │         Select Module
            │              │              │
            └──────────────┴──────────────┘
                           │
                    Code Available
                           │
            ┌──────────────┼──────────────┐
            │                             │
       AI Generation                Pynguin Generation
     (GPT-OSS/Llama)               (Automatic Coverage)
            │                             │
            │                             │
            └──────────────┬──────────────┘
                           │
                    Generated Tests
                           │
            ┌──────────────┼──────────────┐
            │              │              │
         Download    Detect Smells    Use Tests
```

---

**Visual guide complete!** 

This provides a clear understanding of how the UI flows and what users will see at each step of the file and project upload process.
