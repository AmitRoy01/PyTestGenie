# Test Code Refactoring Feature - Documentation

## Overview

This document describes the new **AI-Powered Test Code Refactoring** feature that has been integrated into PyTestGenie. This feature allows users to automatically refactor test code to remove test smells using AI models (Llama 3.2 via Ollama or GPT-OSS via HuggingFace).

## Feature Description

After detecting test smells using the existing smell detection method, users can now refactor their test code using either:
1. **Single Agent Approach** - Fast, direct refactoring by a single AI agent
2. **Multi Agent Approach** - Thorough, iterative refactoring with detection, evaluation, and review phases

## Architecture

### Backend Components

1. **Route Module** (`backend/routes/refactoring.py`)
   - Provides REST API endpoints for refactoring
   - Handles both single-agent and multi-agent refactoring modes
   - Supports Ollama and HuggingFace models

2. **Integration** (`backend/app_unified.py`)
   - Registers the refactoring blueprint at `/api/refactoring`
   - Adds refactoring service to the main API

### Frontend Components

1. **Service** (`frontend/src/services/refactoringService.js`)
   - API client for refactoring endpoints
   - Methods: `getModels()`, `getSmells()`, `checkHealth()`, `refactorCode()`

2. **RefactoringPanel Component** (`frontend/src/components/RefactoringPanel.jsx`)
   - UI for configuring and running refactoring
   - Displays results, including code comparison and multi-agent process details

3. **Updated SmellDetector** (`frontend/src/components/SmellDetector.jsx`)
   - Integrated refactoring button after smell detection
   - Shows/hides RefactoringPanel on demand

## API Endpoints

### GET `/api/refactoring/health`
Check health status of refactoring service

**Response:**
```json
{
  "status": "healthy",
  "ollama_available": true,
  "huggingface_configured": true
}
```

### GET `/api/refactoring/models`
Get available AI models

**Response:**
```json
{
  "ollama": [
    {"name": "Llama 3.2", "model_id": "llama3.2"},
    {"name": "Phi 4", "model_id": "phi4"},
    {"name": "Mistral", "model_id": "mistral"},
    {"name": "CodeLlama", "model_id": "codellama"}
  ],
  "huggingface": [
    {"name": "Mistral 7B Instruct v0.2", "model_id": "mistralai/Mistral-7B-Instruct-v0.2"},
    {"name": "GPT-OSS 20B", "model_id": "openai/gpt-oss-20b:groq"}
  ]
}
```

### GET `/api/refactoring/smells`
Get available test smell types

**Response:**
```json
{
  "smells": [
    "Assertion Roulette",
    "Magic Number Test",
    "Duplicate Assert",
    "Exception Handling",
    "Conditional Test Logic"
  ]
}
```

### POST `/api/refactoring/refactor`
Refactor test code to remove test smells

**Request:**
```json
{
  "code": "test code string",
  "smell_name": "Assertion Roulette",
  "model_type": "ollama",
  "model_name": "llama3.2",
  "agent_mode": "single",
  "temperature": 0.6
}
```

**Response:**
```json
{
  "success": true,
  "refactored_code": "refactored test code",
  "detection_results": [...],  // Only for multi-agent mode
  "error": null
}
```

## User Workflow

### Workflow 1: Integrated with Smell Detection

1. **Detect Test Smells**
   - Go to the "Test Smell Detector" tab
   - Select "Code" mode
   - Paste test code
   - Click "🔍 Analyze Code"

2. **View Detection Results**
   - See detected test smells with their types and line numbers
   - Review the standard HTML report

3. **Refactor Code**
   - Click "🔧 Refactor Code" button (appears after detection)
   - Configure refactoring settings
   - View results

### Workflow 2: Standalone Refactoring

1. **Access Test Code Refactorer**
   - Go to the "Test Code Refactorer" tab

2. **Provide Test Code**
   - **Option A - Paste Code**: Select "📝 Paste Code" and paste your test code
   - **Option B - Upload File**: Select "📄 Upload File" and upload a .py test file

3. **Configure Refactoring**
   - **Test Smell Type**: Select which smell to fix
   - **Agent Mode**: Choose Single or Multi agent
   - **Model Type**: Select Ollama (local) or HuggingFace (API)
   - **Model Name**: Choose specific AI model
   - **Temperature**: Adjust creativity (0.0-1.0)

4. **Refactor and View Results**
   - Click "✨ Refactor with Agent"
   - **Original Code**: Left panel shows the original code
   - **Refactored Code**: Right panel shows the refactored code
   - **Copy Button**: Copy refactored code to clipboard
   - **Multi-Agent Process** (if multi-agent mode): View detailed iterations

## Refactoring Modes

### Single Agent Mode
- **Fast**: Direct refactoring in one step
- **Best for**: Quick fixes, simple refactoring
- **Process**: 
  1. AI analyzes code for the specified smell
  2. AI generates refactored code
  3. Returns result

### Multi Agent Mode
- **Thorough**: Iterative process with multiple verification steps
- **Best for**: Complex smells, high-quality refactoring
- **Process**:
  1. **Detection Phase** (max 3 iterations):
     - Agent 1: Detect smell
     - Agent 2: Evaluate detection
     - Iterate until agreement
  2. **Refactoring Phase** (max 3 iterations):
     - Agent 3: Refactor code
     - Agent 4: Review refactored code
     - Iterate until approval

## Supported Test Smells

1. **Assertion Roulette**
   - Problem: Multiple assertions without explanatory messages
   - Refactoring: Add descriptive messages to each assertion

2. **Magic Number Test**
   - Problem: Numeric literals in assertions
   - Refactoring: Extract to named constants

3. **Duplicate Assert**
   - Problem: Multiple identical assertions
   - Refactoring: Split into separate test methods

4. **Exception Handling**
   - Problem: Manual try-catch in tests
   - Refactoring: Use framework features (e.g., assertThrows)

5. **Conditional Test Logic**
   - Problem: Control statements in tests
   - Refactoring: Create dedicated test methods for each condition

6. **Missing Assertion**
   - Problem: Test method with no assertions
   - Refactoring: Add assertions or convert to helper/fixture

## Configuration

### Ollama (Local Models)
- **Installation**: Install Ollama from https://ollama.com
- **Models**: Automatically pulled when first used
- **No API Key Required**: Runs locally

### HuggingFace (Cloud Models)
- **API Key**: Set in `backend/routes/refactoring.py` or environment variable `HF_TOKEN`
- **Default Key**: Pre-configured (can be updated)
- **Internet Required**: Calls HuggingFace API

## Environment Variables

```bash
# HuggingFace API Token (optional)
HF_TOKEN=your_huggingface_token

# Ollama configuration (optional)
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_ORIGINS=*
```

## File Changes Summary

### New Files
- `backend/routes/refactoring.py` - Refactoring API routes
- `frontend/src/services/refactoringService.js` - API client
- `frontend/src/components/RefactoringPanel.jsx` - Refactoring UI (embedded in SmellDetector)
- `frontend/src/components/TestRefactorer.jsx` - Standalone refactoring component

### Modified Files
- `backend/app_unified.py` - Registered refactoring blueprint
- `frontend/src/App.jsx` - Added TestRefactorer tab and navigation
- `frontend/src/components/SmellDetector.jsx` - Added refactoring integration
- `frontend/src/App.css` - Added refactoring panel styles

### Unchanged Files
All existing features remain intact:
- Test generation (Pynguin, AI)
- Smell detection (file, code, directory, GitHub)
- Authentication system
- Admin panel

## Testing the Feature

1. **Start Backend**:
   ```bash
   cd backend
   python app_unified.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Test Workflow**:
   - Navigate to "Test Smell Detector"
   - Use sample code with test smells
   - Detect smells
   - Click "Refactor Code"
   - Try both Single and Multi agent modes
   - Compare results

## Sample Test Code with Smells

```python
# Example: Assertion Roulette
def test_calculator():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.subtract(10, 3) == 7
    assert calc.multiply(4, 5) == 20
    # Multiple assertions without messages

# Example: Magic Number Test
def test_discount():
    price = 100
    discount = calculate_discount(price)
    assert discount == 10  # Magic number

# Example: Conditional Test Logic
def test_grade(score):
    if score >= 90:
        assert get_grade(score) == 'A'
    elif score >= 80:
        assert get_grade(score) == 'B'
    # Conditional logic in test
```

## Troubleshooting

### Ollama Not Available
- Install Ollama: https://ollama.com
- Start Ollama service: `ollama serve`
- Pull a model: `ollama pull llama3.2`

### HuggingFace Errors
- Check API token is valid
- Verify internet connection
- Try different model

### Refactoring Timeout
- Reduce temperature
- Use smaller code snippets
- Try single-agent mode

### No Smells Detected
- Ensure code actually has test smells
- Try different smell types
- Review detection results

## Performance Considerations

- **Single Agent**: ~5-15 seconds
- **Multi Agent**: ~30-60 seconds (3 iterations)
- **Local Models (Ollama)**: Depends on hardware
- **Cloud Models (HuggingFace)**: Depends on network

## Future Enhancements

Potential improvements:
- Batch refactoring for multiple files
- Custom smell definitions
- Refactoring history
- A/B comparison of different refactoring strategies
- Integration with test generation flow
- Support for more AI models

## Conclusion

The AI-Powered Test Code Refactoring feature seamlessly integrates with PyTestGenie's existing smell detection capabilities, providing users with an end-to-end solution for identifying and fixing test smells. The dual-mode approach (single/multi agent) gives users flexibility in choosing between speed and thoroughness.
