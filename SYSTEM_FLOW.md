# PyTestGenie - System Flow Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      App.jsx                              │  │
│  │            (Tab Navigation Component)                     │  │
│  │                                                            │  │
│  │  ┌────────────────────┐    ┌────────────────────────┐   │  │
│  │  │  TestGenerator.jsx │    │  SmellDetector.jsx     │   │  │
│  │  │  🚀 Generate Tests │    │  🔍 Detect Smells      │   │  │
│  │  └────────────────────┘    └────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/AJAX (Axios)
                             │ SSE (EventSource)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND API                             │
│                  http://localhost:5000                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   app_unified.py                          │  │
│  │              (Main Application Factory)                   │  │
│  │                                                            │  │
│  │  ┌────────────────────┐    ┌────────────────────────┐   │  │
│  │  │  test_generation.py│    │  smell_detection.py    │   │  │
│  │  │  (Routes Blueprint)│    │  (Routes Blueprint)    │   │  │
│  │  └─────────┬──────────┘    └──────────┬─────────────┘   │  │
│  └────────────┼───────────────────────────┼─────────────────┘  │
│               │                           │                     │
│               ▼                           ▼                     │
│  ┌────────────────────────┐    ┌────────────────────────┐     │
│  │  test_generator/       │    │  smell_detector/       │     │
│  │  (Module)              │    │  (Module)              │     │
│  │                        │    │                        │     │
│  │  ├─ pynguin_generator  │    │  ├─ analyzer.py       │     │
│  │  ├─ ai_generator       │    │  ├─ detector.py       │     │
│  │  └─ models.py          │    │  ├─ python_parser.py  │     │
│  │                        │    │  └─ report_generator  │     │
│  └────────────────────────┘    └────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
    ┌───────────┐                  ┌──────────┐
    │  Pynguin  │                  │   HTML   │
    │  OpenAI   │                  │  Report  │
    │   APIs    │                  │  ./report│
    └───────────┘                  └──────────┘
```

## Request Flow: Test Generation

```
1. User Input
   └─> Paste code in TestGenerator.jsx
       └─> Select method (Pynguin or AI)

2. Frontend Request
   └─> POST /api/test-generator/generate-tests/pynguin
       OR
   └─> POST /api/test-generator/generate-tests/ai

3. Backend Processing
   └─> routes/test_generation.py receives request
       └─> Calls appropriate generator:
           ├─> PynguinGenerator.generate_tests()
           │   └─> Spawns subprocess
           │       └─> Streams logs via SSE
           │
           └─> AITestGenerator.generate_tests()
               └─> Calls OpenAI API
                   └─> Returns immediately

4. Response
   └─> Test code returned to frontend
       └─> Displayed in TestGenerator.jsx
           └─> User can download or detect smells
```

## Request Flow: Smell Detection

```
1. User Input (Multiple Options)
   ├─> Paste code
   ├─> Upload file
   ├─> Upload directory
   └─> Enter GitHub URL

2. Frontend Request
   └─> POST /api/smell-detector/analyze/[code|file|directory|github]

3. Backend Processing
   └─> routes/smell_detection.py receives request
       └─> Calls TestSmellAnalyzer
           ├─> Save/clone files if needed
           ├─> Parse Python files
           ├─> Run detection algorithms
           └─> Generate HTML report

4. Response
   └─> Analysis results returned
       └─> Displayed in SmellDetector.jsx
           └─> User clicks "View Report"
               └─> Opens ./report/log.html
```

## Pipeline Integration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATED PIPELINE                       │
│                                                              │
│  Step 1: Generate Tests                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ User pastes code → Generates tests → Views results │    │
│  └────────────────────────┬───────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  Step 2: Detect Smells (Automatic Bridge)                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Clicks "Detect Smells" → Sends generated code      │    │
│  │ to smell detector → Views analysis                 │    │
│  └────────────────────────┬───────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  Step 3: Review & Export                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Views HTML report → Downloads clean tests          │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Module Interactions

```
┌─────────────────────────────────────────────────────┐
│              test_generator Module                   │
│                                                      │
│  ┌──────────────────┐                              │
│  │ pynguin_generator│──┐                           │
│  └──────────────────┘  │                           │
│                        │ Both implement            │
│  ┌──────────────────┐  │ generate_tests()         │
│  │   ai_generator   │──┘                           │
│  └──────────────────┘                               │
│                                                      │
│  Returns: TestGenerationResult                      │
│           (test_code, error, method)                │
└─────────────────────────────────────────────────────┘
                        │
                        │ test_code
                        ▼
┌─────────────────────────────────────────────────────┐
│             smell_detector Module                    │
│                                                      │
│  ┌──────────────────┐                              │
│  │    analyzer.py   │ ← Coordinates detection      │
│  └────────┬─────────┘                              │
│           │                                          │
│           ├──→ python_parser.py (Parse AST)        │
│           ├──→ detector.py (Detect smells)         │
│           └──→ report_generator.py (HTML report)   │
│                                                      │
│  Returns: Analysis results + HTML report            │
└─────────────────────────────────────────────────────┘
```

## Data Models

```
TestGenerationResult
├── test_code: str       # Generated test code
├── error: Optional[str] # Error message if failed
└── method: str          # 'pynguin' or 'ai'

AnalysisResult
├── filepath: str        # File path analyzed
├── logs: List[Log]      # Detected smells
└── smell_count: int     # Total smells found

Log (Smell Detection)
├── test_smell_type: str # Type of smell
├── method_name: str     # Method with smell
└── lines: str           # Line numbers
```

## Component State Management

```
TestGenerator Component State:
├── code: string              # User input code
├── testCode: string          # Generated tests
├── loading: boolean          # Generation in progress
├── logs: array               # Pynguin logs
├── useAI: boolean            # AI vs Pynguin
└── canDetectSmells: boolean  # Enable smell button

SmellDetector Component State:
├── mode: string              # code/file/directory/github
├── code: string              # Input code (if mode=code)
├── githubUrl: string         # GitHub URL (if mode=github)
├── loading: boolean          # Analysis in progress
└── results: object           # Analysis results
```

## Configuration Flow

```
.env File
    │
    ▼
config/settings.py
    │
    ├──→ Config class (base)
    ├──→ DevelopmentConfig
    └──→ ProductionConfig
         │
         ▼
    app_unified.py
         │
         ▼
    Application Runtime
```

## Error Handling Flow

```
Frontend Component
    │ try-catch
    ▼
Axios Request
    │ HTTP errors
    ▼
Backend Route
    │ try-catch
    ▼
Module Function
    │ try-catch, validation
    ▼
External Service (Pynguin/OpenAI)
    │ error responses
    ▼
Result Object (error field)
    │
    ▼
Frontend Display (alert/UI)
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Production Setup                    │
│                                                      │
│  ┌────────────────────┐    ┌────────────────────┐  │
│  │  Frontend (Nginx)  │    │  Backend (Gunicorn) │  │
│  │  Static Files      │    │  Flask App          │  │
│  │  Port 80/443       │    │  Port 5000          │  │
│  └────────┬───────────┘    └─────────┬──────────┘  │
│           │                          │              │
│           └──────────┬───────────────┘              │
│                      │                               │
│                      ▼                               │
│            ┌──────────────────┐                     │
│            │   Load Balancer   │                     │
│            └──────────────────┘                     │
└─────────────────────────────────────────────────────┘
```

## File Organization Visual

```
backend/
│
├── [ENTRY POINT]
│   └── app_unified.py ⭐ Start here
│
├── [CONFIGURATION]
│   └── config/settings.py
│
├── [API LAYER]
│   └── routes/
│       ├── test_generation.py
│       └── smell_detection.py
│
└── [BUSINESS LOGIC]
    └── modules/
        ├── test_generator/     ← Test generation
        └── smell_detector/     ← Smell detection

frontend/
│
├── [ENTRY POINT]
│   ├── index.html
│   └── src/index.jsx ⭐ Start here
│
├── [MAIN APP]
│   ├── src/App.jsx ⭐ Tab navigation
│   └── src/App.css
│
└── [FEATURES]
    └── src/components/
        ├── TestGenerator.jsx   ← Test gen UI
        └── SmellDetector.jsx   ← Smell detect UI
```

This visual documentation makes it easy to understand:
- ✅ System architecture
- ✅ Request flows
- ✅ Module interactions
- ✅ Data models
- ✅ File organization
- ✅ Entry points
