# PyTestGenie AI Model Integration Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                          │
│                    TestGenerator.jsx                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Selects Method:                                            │
│  ┌────────────────┐  ┌──────────────────────────────┐          │
│  │  🤖 Pynguin    │  │  🧠 AI (OpenAI/HuggingFace)  │          │
│  └────────────────┘  └──────────────────────────────┘          │
│         │                          │                             │
│         │                          ▼                             │
│         │             ┌──────────────────────────┐              │
│         │             │  🤖 AI Model Selector    │              │
│         │             ├──────────────────────────┤              │
│         │             │ □ GPT-OSS 20B (Cloud)    │              │
│         │             │ □ Llama 3.2 (Local)      │              │
│         │             └──────────────────────────┘              │
│         │                          │                             │
│         │                          │                             │
└─────────┼──────────────────────────┼─────────────────────────────┘
          │                          │
          │ POST /generate-tests/    │ POST /generate-tests/ai
          │     pynguin              │     {code, model}
          │                          │
┌─────────▼──────────────────────────▼─────────────────────────────┐
│                    Backend (Flask)                                │
│                 routes/test_generation.py                         │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐      ┌──────────────────────────────┐  │
│  │ PynguinGenerator    │      │   AITestGenerator            │  │
│  │   (Automatic)       │      │   (model_name parameter)     │  │
│  └─────────────────────┘      └──────────────────────────────┘  │
│                                            │                      │
│                                            ▼                      │
│                               ┌──────────────────────┐           │
│                               │  Model Configuration │           │
│                               ├──────────────────────┤           │
│                               │ model == "gpt-oss"?  │           │
│                               └──────────┬───────────┘           │
│                                          │                        │
│                          ┌───────────────┴───────────────┐       │
│                          │                               │       │
│                         YES                             NO       │
│                          │                               │       │
└──────────────────────────┼───────────────────────────────┼───────┘
                           │                               │
                           ▼                               ▼
          ┌────────────────────────────┐   ┌──────────────────────────┐
          │   HuggingFace Router       │   │   Local Ollama Server    │
          │   router.huggingface.co    │   │   localhost:11434        │
          ├────────────────────────────┤   ├──────────────────────────┤
          │ Model: gpt-oss-20b:groq    │   │ Model: llama3.2          │
          │ Auth: HF_TOKEN required    │   │ Auth: Not required       │
          │ Network: Internet needed   │   │ Network: Local only      │
          │ Cost: Per API call         │   │ Cost: Free               │
          │ Privacy: Cloud-based       │   │ Privacy: On-device       │
          └────────────────────────────┘   └──────────────────────────┘
                           │                               │
                           └───────────────┬───────────────┘
                                           │
                                    Generated Tests
                                           │
                           ┌───────────────▼───────────────┐
                           │     Python Test Code          │
                           │     (pytest format)           │
                           └───────────────────────────────┘
```

## Request/Response Flow

### 1. GPT-OSS Flow
```
User → Select "GPT-OSS 20B" → Paste Code → Generate
  ↓
Frontend sends: {code: "...", model: "gpt-oss"}
  ↓
Backend routes/test_generation.py
  ↓
AITestGenerator(model_name="gpt-oss")
  ↓
Configure OpenAI client:
  - base_url: https://router.huggingface.co/v1
  - api_key: HF_TOKEN (from env)
  - model: openai/gpt-oss-20b:groq
  ↓
Send request to HuggingFace
  ↓
Receive and parse response
  ↓
Return: {test_code: "...", method: "ai-gpt-oss", model_used: "gpt-oss"}
  ↓
Frontend displays generated tests
```

### 2. Llama 3.2 Flow
```
User → Select "Llama 3.2 (Local)" → Paste Code → Generate
  ↓
Frontend sends: {code: "...", model: "llama-3.2"}
  ↓
Backend routes/test_generation.py
  ↓
AITestGenerator(model_name="llama-3.2")
  ↓
Configure OpenAI client:
  - base_url: http://localhost:11434/v1
  - api_key: "ollama" (dummy, not used)
  - model: llama3.2
  ↓
Send request to local Ollama server
  ↓
Receive and parse response
  ↓
Return: {test_code: "...", method: "ai-llama-3.2", model_used: "llama-3.2"}
  ↓
Frontend displays generated tests
```

## Component Interactions

```
┌──────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TestGenerator.jsx                                               │
│  ├── State Management:                                           │
│  │   ├── useAI (boolean) - AI vs Pynguin                        │
│  │   ├── aiModel (string) - "gpt-oss" | "llama-3.2"             │
│  │   ├── algorithm (string) - For Pynguin mode                  │
│  │   └── code, testCode, loading, etc.                          │
│  │                                                               │
│  ├── UI Components:                                              │
│  │   ├── Method Selector (Radio: Pynguin | AI)                  │
│  │   ├── Algorithm Dropdown (shown if !useAI)                   │
│  │   ├── Model Dropdown (shown if useAI) ← NEW                  │
│  │   └── Generate Button                                        │
│  │                                                               │
│  └── API Calls:                                                  │
│      ├── axios.post('/generate-tests/ai', {code, model})        │
│      └── axios.post('/generate-tests/pynguin', {code, algo})    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Request
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Backend Layer                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  routes/test_generation.py                                       │
│  ├── @route('/generate-tests/ai')                               │
│  │   ├── Extract: code, model (default "gpt-oss")               │
│  │   ├── Create: AITestGenerator(model_name=model)              │
│  │   ├── Call: generator.generate_tests(code)                   │
│  │   └── Return: {test_code, method, model_used}                │
│  │                                                               │
│  └── @route('/generate-tests/pynguin')                          │
│      └── [Unchanged - existing Pynguin logic]                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ Instantiate
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      AI Generator Module                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  modules/test_generator/ai_generator.py                          │
│  │                                                               │
│  ├── class AITestGenerator:                                      │
│  │   │                                                           │
│  │   ├── MODELS = {                                             │
│  │   │     "gpt-oss": {...},  ← Cloud config                    │
│  │   │     "llama-3.2": {...} ← Local config                    │
│  │   │   }                                                       │
│  │   │                                                           │
│  │   ├── __init__(model_name, hf_token=None, llama_url=None):  │
│  │   │   ├── Validate model_name in MODELS                      │
│  │   │   ├── Load model config                                  │
│  │   │   ├── Set api_key (HF_TOKEN or dummy)                    │
│  │   │   ├── Set base_url (cloud or local)                      │
│  │   │   └── Create OpenAI client                               │
│  │   │                                                           │
│  │   └── generate_tests(code):                                  │
│  │       ├── Validate input code (ast.parse)                    │
│  │       ├── Create chat completion request                     │
│  │       ├── Extract and validate test code                     │
│  │       └── Return TestGenerationResult                        │
│  │                                                               │
│  └── Helper functions:                                           │
│      ├── extract_test_code(ai_response)                         │
│      └── format_prompt(code)                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ API Call
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                       External Services                          │
├─────────────────────────────┬────────────────────────────────────┤
│                             │                                    │
│  HuggingFace Router         │     Local Ollama Server            │
│  (if model="gpt-oss")       │     (if model="llama-3.2")         │
│  ────────────────────       │     ──────────────────             │
│  • URL: router.hf.co/v1     │     • URL: localhost:11434/v1      │
│  • Auth: Required (token)   │     • Auth: None                   │
│  • Model: gpt-oss-20b:groq  │     • Model: llama3.2              │
│  • Internet: Required       │     • Internet: Not required       │
│                             │                                    │
└─────────────────────────────┴────────────────────────────────────┘
```

## Configuration Flow

```
Environment Variables (.env)
├── HF_TOKEN=xxx                    → Used by GPT-OSS
├── LLAMA_API_URL=http://...        → Used by Llama 3.2
└── [other configs]

         ↓ loaded by

config/settings.py
├── class Config:
│   ├── HF_TOKEN = os.getenv('HF_TOKEN')
│   ├── LLAMA_API_URL = os.getenv('LLAMA_API_URL', 'http://localhost:11434/v1')
│   └── [other settings]

         ↓ used by

AITestGenerator.__init__()
├── if model requires HF token:
│   └── api_key = hf_token or os.getenv("HF_TOKEN")
└── else:
    └── api_key = "ollama" (dummy)
    └── base_url = llama_url or os.getenv("LLAMA_API_URL")
```

## Data Flow Example

### Example: User generates tests with Llama 3.2

```
Step 1: User Input
──────────────────
Code: "def add(a, b): return a + b"
Method: AI
Model: llama-3.2

Step 2: Frontend State
──────────────────────
{
  code: "def add(a, b): return a + b",
  useAI: true,
  aiModel: "llama-3.2"
}

Step 3: API Request
───────────────────
POST http://localhost:5000/api/test-generator/generate-tests/ai
Body: {
  "code": "def add(a, b): return a + b",
  "model": "llama-3.2"
}

Step 4: Backend Processing
───────────────────────────
generator = AITestGenerator(model_name="llama-3.2")
  → Loads config: MODELS["llama-3.2"]
  → Sets base_url: http://localhost:11434/v1
  → Creates OpenAI client with local endpoint

Step 5: Ollama API Call
────────────────────────
POST http://localhost:11434/v1/chat/completions
Body: {
  "model": "llama3.2",
  "messages": [
    {"role": "system", "content": "You are a Python testing expert..."},
    {"role": "user", "content": "Generate tests for: def add(a, b): return a + b"}
  ],
  "temperature": 0.7
}

Step 6: Response Processing
────────────────────────────
Raw Response: "```python\nimport pytest\n\ndef test_add():\n..."
  → extract_test_code() removes markdown
  → ast.parse() validates syntax
  → Returns TestGenerationResult

Step 7: API Response
────────────────────
{
  "test_code": "import pytest\n\ndef test_add():\n...",
  "method": "ai-llama-3.2",
  "model_used": "llama-3.2"
}

Step 8: Frontend Display
─────────────────────────
• Updates testCode state
• Renders in code output box
• Enables "Detect Test Smells" button
• Enables "Download" button
```

## Key Design Decisions

### 1. Model Configuration Dictionary
```python
MODELS = {
    "model-key": {
        "name": "Display Name",
        "model_id": "API Model ID",
        "base_url": "API Endpoint",
        "requires_hf_token": bool
    }
}
```
**Benefits**:
- Easy to add new models
- Centralized configuration
- Clear model requirements
- Self-documenting

### 2. Unified OpenAI Client
- Use OpenAI SDK for both models
- Ollama implements OpenAI-compatible API
- Single code path for all models
- Consistent error handling

### 3. Backward Compatibility
- Default model: "gpt-oss"
- Existing API calls work unchanged
- No breaking changes
- Gradual migration possible

### 4. Frontend Model Selector
- Only shown when AI mode selected
- Styled consistently with algorithm selector
- Clear labels indicating cloud vs local
- State managed independently

---

**Architecture designed for extensibility and maintainability!**
