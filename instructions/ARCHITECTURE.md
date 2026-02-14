# PyTestGenie - Architecture Documentation

## 6.1 Architectural Context Diagram

The Architectural Context Diagram illustrates PyTestGenie's position within its operational environment, showing the system boundaries, external actors, external systems, and key interactions. This high-level view demonstrates how PyTestGenie integrates with users, third-party services, and infrastructure components.

### Context Diagram

```
                                    ┌─────────────────────┐
                                    │   Regular User      │
                                    │   (Primary Actor)   │
                                    └──────────┬──────────┘
                                               │
                                               │ Uploads code
                                               │ Generates tests
                                               │ Views reports
                                               │
                    ┌──────────────────────────▼────────────────────────────┐
                    │                                                        │
  ┌─────────────┐   │                                                        │   ┌─────────────────┐
  │    Admin    │   │                                                        │   │   LLM Services  │
  │    User     │───┤                  PyTestGenie System                   │◄──│  (External)     │
  └─────────────┘   │                                                        │   │                 │
      │             │  ┌──────────────────────────────────────────────┐    │   │  - Gemini API   │
      │             │  │  Frontend (React/Vite)                       │    │   │  - GPT API      │
      │             │  │  - User Interface                            │    │   │  - Llama        │
      │ Manages     │  │  - Dashboard                                 │    │   │  - HuggingFace  │
      │ users       │  │  - Authentication UI                         │    │   └─────────────────┘
      │             │  └────────────────────┬─────────────────────────┘    │            │
      │             │                       │ HTTP/REST API                │            │
      │             │                       │                              │            │
      │             │  ┌────────────────────▼──────────────────────────┐  │            │
      │             │  │  Backend (Flask/Python)                       │  │            │
      │             │  │                                               │  │            │
      │             │  │  ┌─────────────────────────────────────────┐ │  │   API Calls│
      │             │  │  │  Core Modules                           │ │◄─┼────────────┘
      │             │  │  │                                         │ │  │
      │             │  │  │  • TestCodeGenerator                   │ │  │
      │             │  │  │  • TestSmellDetector                   │ │  │
      │             │  │  │  • RefactoringEngine                   │ │  │
      │             │  │  │  • LLMModelManager                     │ │  │
      │             │  │  │  • ReportManager                       │ │  │
      │             │  │  │  • ArtifactLibraryManager             │ │  │
      │             │  │  └─────────────────────────────────────────┘ │  │
      │             │  │                                               │  │
      │             │  └───────────────┬─────────────────┬─────────────┘  │
      │             │                  │                 │                │
      │             │                  │                 │                │
      │             └──────────────────┼─────────────────┼────────────────┘
                                       │                 │
                                       │                 │
                    ┌──────────────────▼────┐   ┌───────▼────────────────┐
                    │   Database            │   │   File System          │
                    │   (PostgreSQL/SQLite) │   │   (Storage)            │
                    │                       │   │                        │
                    │   • User Data         │   │   • Source Code        │
                    │   • Projects          │   │   • Generated Tests    │
                    │   • Test Metadata     │   │   • Reports            │
                    │   • Smell Reports     │   │   • Refactored Code    │
                    │   • Evaluation Data   │   │   • Artifacts          │
                    └───────────────────────┘   └────────────────────────┘
                                       │
                                       │
                                       │
                    ┌──────────────────▼────────────────┐
                    │   Email Service (SMTP)            │
                    │   (External)                      │
                    │                                   │
                    │   • Registration Confirmation     │
                    │   • Account Approval Notification │
                    │   • System Alerts                 │
                    └───────────────────────────────────┘


                    ┌──────────────────────────────────────┐
                    │   Pynguin (External Tool)            │
                    │   Integrated via Python API          │
                    │                                      │
                    │   • Search-Based Test Generation     │
                    │   • Coverage Analysis                │
                    └──────────────────────────────────────┘
```

### System Boundary

**PyTestGenie System** encompasses:
- Frontend application (React/Vite web interface)
- Backend application (Flask REST API server)
- Core business logic modules (8 analysis classes)
- Internal data processing and orchestration

**External to PyTestGenie:**
- Users (Admin, Regular Users)
- LLM Service Providers (Gemini, GPT, Llama, HuggingFace)
- Database management system
- File system storage
- Email service
- Pynguin tool

---

## 6.2 External System Interactions

### 1. User Interactions (Primary Actors)

#### Regular User
**Direction**: Bidirectional  
**Protocol**: HTTPS (REST API)  
**Data Exchanged**:
- **To System**: Python source code, configuration preferences, test generation requests, detection parameters
- **From System**: Generated tests, smell detection reports, refactored code, evaluation reports

**Key Use Cases**:
- Upload/paste Python code
- Generate unit tests
- Detect test smells
- Request refactoring
- View and export reports
- Manage user library

#### Admin User
**Direction**: Bidirectional  
**Protocol**: HTTPS (REST API)  
**Data Exchanged**:
- **To System**: User approval decisions, system configurations
- **From System**: Pending user registrations, system statistics, user activity logs

**Key Use Cases**:
- Approve/reject user registrations
- View user management dashboard
- Monitor system health

---

### 2. LLM Service Providers (External Systems)

#### Google Gemini API
**Direction**: Bidirectional  
**Protocol**: HTTPS (REST API)  
**Authentication**: API Key  
**Data Exchanged**:
- **To LLM**: Prompts for test generation, smell detection, code refactoring
- **From LLM**: Generated test code, detected smells with explanations, refactored code suggestions

**Usage Context**:
- Semantic test generation
- LLM-based smell detection
- Multi-agent refactoring workflows

#### OpenAI GPT API
**Direction**: Bidirectional  
**Protocol**: HTTPS (REST API)  
**Authentication**: API Key  
**Data Exchanged**:
- **To LLM**: Structured prompts with code context
- **From LLM**: AI-generated responses (tests, analysis, refactorings)

**Usage Context**:
- Alternative LLM for generation and detection
- Comparative analysis experiments

#### Llama / HuggingFace
**Direction**: Bidirectional  
**Protocol**: HTTPS (API) or Local Model  
**Authentication**: API Key (if cloud) or Local  
**Data Exchanged**:
- **To LLM**: Code and prompts
- **From LLM**: Generated outputs

**Usage Context**:
- Open-source LLM alternative
- Local deployment option

---

### 3. Database System (PostgreSQL/SQLite)

**Direction**: Bidirectional  
**Protocol**: Database Connection (SQL)  
**Data Exchanged**:
- **To Database**: User records, project data, test metadata, smell reports, evaluation metrics
- **From Database**: Query results, stored artifacts metadata, user information

**Stored Entities**:
- User accounts and authentication data
- Projects and source file metadata
- Generated test records
- Smell detection reports
- Refactored code versions
- Evaluation reports

**Operations**:
- CRUD operations for all entities
- Complex queries for reporting and statistics
- Transaction management for data integrity

---

### 4. File System (Storage)

**Direction**: Bidirectional  
**Protocol**: File I/O  
**Data Stored**:
- Uploaded Python source files
- Generated test files
- HTML/PDF report files
- Refactored code versions
- User library artifacts

**Operations**:
- File upload and storage
- File retrieval and download
- File deletion
- Directory organization

**Storage Structure**:
```
uploads/
  ├── user_{id}/
  │   ├── projects/
  │   │   ├── project_{id}/
  │   │   │   ├── source_files/
  │   │   │   ├── generated_tests/
  │   │   │   └── reports/
```

---

### 5. Email Service (SMTP)

**Direction**: Unidirectional (Outbound)  
**Protocol**: SMTP  
**Authentication**: SMTP credentials  
**Data Sent**:
- Registration confirmation emails
- Account approval notifications
- Password reset links
- System alerts

**Triggered By**:
- New user registration
- Admin approval/rejection
- System events

---

### 6. Pynguin (External Tool)

**Direction**: Bidirectional  
**Protocol**: Python API / Command-line interface  
**Integration**: Embedded as Python library  
**Data Exchanged**:
- **To Pynguin**: Source code, configuration (algorithm, time budget)
- **From Pynguin**: Generated test files, coverage metrics, execution logs

**Usage Context**:
- Rule-based test generation
- High coverage test creation
- Structural testing

---

## 6.3 Data Flow Summary

### Inbound Data Flows

| Source | Data | Destination | Purpose |
|--------|------|-------------|---------|
| Regular User | Python source code | Backend → ArtifactLibraryManager | Test generation input |
| Regular User | Test generation requests | Backend → TestCodeGenerator | Initiate test creation |
| Admin User | Approval decisions | Backend → UserManager | User account management |
| LLM Services | Generated tests, analyses | Backend → Core Modules | AI-powered functionality |
| Database | User/project data | Backend | Data retrieval |
| File System | Stored artifacts | Backend | File retrieval |

### Outbound Data Flows

| Source | Data | Destination | Purpose |
|--------|------|-------------|---------|
| Backend | Generated tests | User browser | Display results |
| Backend | Detection reports | User browser | Show smell analysis |
| Backend | User data | Database | Persist information |
| Backend | Artifacts | File System | Store files |
| Backend | Prompts | LLM Services | Request AI processing |
| Backend | Email notifications | Email Service | User communication |

---

## 6.4 System Integration Points

### 1. Frontend ↔ Backend Integration
- **Technology**: REST API over HTTPS
- **Format**: JSON
- **Authentication**: JWT tokens
- **Endpoints**: ~20 API routes for all functionality

### 2. Backend ↔ LLM Services Integration
- **Technology**: HTTP REST APIs
- **Format**: JSON
- **Rate Limiting**: Managed by LLMModelManager
- **Error Handling**: Retry logic, fallback mechanisms

### 3. Backend ↔ Database Integration
- **Technology**: SQLAlchemy ORM
- **Connection Pooling**: Yes
- **Migration**: Alembic for schema changes

### 4. Backend ↔ File System Integration
- **Technology**: Python file I/O
- **Security**: Path validation, user isolation
- **Quota Management**: Storage limits per user

---

## 6.5 Security Boundaries

### Authentication Boundary
- All user requests require authentication (except registration/login)
- JWT token validation at middleware level
- Role-based access control (Admin vs User)

### External API Security
- API keys stored securely (environment variables)
- HTTPS for all external communications
- Rate limiting to prevent abuse

### Data Security
- Password hashing (bcrypt)
- Sensitive data encryption
- User data isolation

---

## 6.6 Deployment Context

### Development Environment
- Frontend: Vite dev server (http://localhost:5173)
- Backend: Flask dev server (http://localhost:5000)
- Database: SQLite (local file)

### Production Environment
- Frontend: Static files served via Nginx/Apache
- Backend: Gunicorn + Flask (behind reverse proxy)
- Database: PostgreSQL server
- File Storage: Dedicated storage volume

---

## 6.7 Architectural Patterns and Styles

### 6.7.1 Pipe and Filter Architecture

PyTestGenie employs a **Pipe and Filter architectural pattern** as the core design for its automated testing pipeline. This pattern is ideal for systems that require sequential data transformation through multiple processing stages, where each stage (filter) performs a specific operation and passes the result to the next stage through connectors (pipes).

#### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         PyTestGenie Pipeline                                 │
│                                                                              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────┐│
│  │   Input     │      │   Filter 1  │      │   Filter 2  │      │ Filter 3││
│  │  (Source    │─────>│    Test     │─────>│    Test     │─────>│  Smell  ││
│  │   Code)     │ Pipe │ Generation  │ Pipe │   Smell     │ Pipe │Refactor ││
│  └─────────────┘  1   │             │  2   │  Detection  │  3   │         ││
│                       └─────────────┘      └─────────────┘      └─────┬───┘│
│                                                                         │    │
│                                                                    Pipe │    │
│                                                                      4  │    │
│                                                                         ▼    │
│                                                               ┌─────────────┐│
│                                                               │   Filter 4  ││
│                                                               │   Report    ││
│                                                               │  Generation ││
│                                                               └──────┬──────┘│
│                                                                      │       │
│                                                                      ▼       │
│                                                               ┌─────────────┐│
│                                                               │   Output    ││
│                                                               │ (Reports &  ││
│                                                               │  Artifacts) ││
│                                                               └─────────────┘│
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Filters (Processing Components)

##### Filter 1: Test Code Generator
**Input**: Python source code, generation configuration  
**Processing**:
- Parses and analyzes source code structure
- Applies Pynguin algorithms (RANDOOPY, MIO, WHOLE_SUITE) for structural test generation
- OR invokes LLM services for semantic test generation
- Validates generated tests for syntax correctness
- Calculates initial coverage metrics

**Output**: Generated unit test code, coverage metrics  
**Implementation**: `TestCodeGenerator` class  
**Technologies**: Pynguin library, LLM APIs (Gemini, GPT)

**Characteristics**:
- Stateless operation
- Can operate in two modes: rule-based or AI-assisted
- Produces intermediate artifact (test code)

---

##### Filter 2: Test Smell Detector
**Input**: Generated test code from Filter 1  
**Processing**:
- Parses test code into Abstract Syntax Tree (AST)
- Applies rule-based detection (TEMPY/PyNOSE patterns)
- OR performs LLM-based semantic analysis
- OR executes multi-agent analysis for consensus
- Classifies detected smells by type and severity
- Calculates confidence scores

**Output**: Smell detection report with identified issues, locations, and explanations  
**Implementation**: `TestSmellDetector` class  
**Technologies**: Python AST, Pattern matching, LLM APIs

**Characteristics**:
- Multiple detection strategies (rule-based, LLM, multi-agent)
- Annotates code with smell metadata
- Produces structured detection report

**Detected Smells**:
- Assertion Roulette, Eager Test, Lazy Test
- Mystery Guest, Resource Optimism
- Test Code Duplication, Magic Number Test
- Conditional Test Logic

---

##### Filter 3: Smell Refactorer
**Input**: Test code with detected smells from Filter 2  
**Processing**:
- Analyzes each detected smell and its context
- Applies appropriate refactoring strategies
- Uses LLM for complex transformations
- OR orchestrates multi-agent workflow:
  - Analyzer Agent: Reviews smell context
  - Refactorer Agent: Proposes solutions
  - Reviewer Agent: Validates proposals
  - Validator Agent: Ensures behavior preservation
- Executes refactoring transformations
- Validates refactored code preserves test behavior

**Output**: Refactored test code, validation results, transformation explanations  
**Implementation**: `RefactoringEngine` class  
**Technologies**: LLM APIs, AST manipulation

**Characteristics**:
- Behavior-preserving transformations
- Multiple agent collaboration
- Validation checkpoints

**Refactoring Strategies**:
- Extract method for duplicated code
- Add assertion messages
- Split eager tests
- Remove unnecessary dependencies
- Add resource cleanup

---

##### Filter 4: Report Generator
**Input**: Original code, generated tests, smell reports, refactored code from all previous filters  
**Processing**:
- Aggregates metrics from all pipeline stages
- Calculates detection accuracy (precision, recall, F1-score)
- Computes refactoring success rates
- Measures coverage improvement
- Performs comparative analysis (rule-based vs LLM)
- Generates visualizations and charts
- Formats report in selected format (HTML, PDF, JSON)

**Output**: Comprehensive evaluation report with metrics, comparisons, and insights  
**Implementation**: `ReportManager` class  
**Technologies**: Jinja2 templates, Chart.js, Matplotlib

**Characteristics**:
- Aggregation point for all pipeline data
- Multiple output formats
- Statistical analysis and visualization

---

#### Pipes (Data Connectors)

##### Pipe 1: Source Code → Test Generation
**Data Format**: Python source code (string or file)  
**Metadata**: File name, user preferences, algorithm selection  
**Storage**: `ArtifactLibraryManager` saves source file  
**Validation**: Syntax checking, Python version compatibility

---

##### Pipe 2: Generated Tests → Smell Detection
**Data Format**: Generated test code (Python file)  
**Metadata**: Generation method, coverage percentage, execution time  
**Storage**: Tests stored in user library  
**Validation**: Valid Python syntax, executable tests

---

##### Pipe 3: Smell Report → Refactoring
**Data Format**: Detected smells with locations and types  
**Metadata**: Detection method, confidence scores, severity levels  
**Storage**: Detection report stored in database  
**Validation**: Valid smell types, correct line numbers

---

##### Pipe 4: Refactored Code → Report Generation
**Data Format**: Refactored test code, validation results  
**Metadata**: Refactoring method, transformation applied, validation status  
**Storage**: Refactored code stored in user library  
**Validation**: Behavior preservation verified

---

#### Key Characteristics of the Pipeline

##### 1. Sequential Processing
Each filter executes in order, building upon the output of the previous filter:
```
Source Code → Tests → Smells → Refactored Code → Report
```

##### 2. Data Transformation
Each filter transforms its input into a new form:
- **Filter 1**: Code → Tests
- **Filter 2**: Tests → Smell Report
- **Filter 3**: Smelly Tests → Clean Tests
- **Filter 4**: All Data → Evaluation Report

##### 3. Filter Independence
Each filter is:
- **Self-contained**: Operates independently
- **Reusable**: Can be used in different contexts
- **Replaceable**: Implementation can change without affecting other filters
- **Testable**: Can be tested in isolation

##### 4. Incremental Processing
Users can:
- Stop after any filter to inspect intermediate results
- Re-run individual filters with different configurations
- Skip filters if not needed (e.g., skip refactoring)

##### 5. Multiple Paths
The pipeline supports alternative processing paths:
```
Source → [Pynguin OR LLM] → Tests
Tests → [Rule-based OR LLM OR Multi-Agent] → Smells
Smells → [LLM OR Multi-Agent] → Refactored Code
```

---

#### Advantages of Pipe and Filter for PyTestGenie

##### 1. Modularity
- Each filter (class) has a single, well-defined responsibility
- Easy to understand and maintain
- Changes to one filter don't affect others

##### 2. Flexibility
- Filters can be added, removed, or reordered
- Alternative implementations can be swapped (e.g., different LLM models)
- Parallel execution possible for independent filters

##### 3. Reusability
- Individual filters can be used in different workflows
- Detection filter can analyze existing tests (not just generated ones)
- Report generator can summarize any pipeline stage

##### 4. Scalability
- Each filter can be optimized independently
- Resource-intensive filters can be distributed
- Caching can be added at pipe boundaries

##### 5. Testability
- Each filter can be unit tested independently
- Integration tests can verify pipe connections
- Mock data can be injected at any pipe

##### 6. User Control
- Users can choose to execute partial pipelines
- Intermediate results visible at each stage
- Configuration changes affect individual filters

---

#### Data Flow Example

**Complete Pipeline Execution:**

```
┌──────────────────────────────────────────────────────────────────────┐
│ User Action: Upload triangle.py                                     │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PIPE 1: Source Code Input                                            │
│ Data: def area(a,b,c): return sqrt(s*(s-a)*(s-b)*(s-c))            │
│ Metadata: filename="triangle.py", language="Python 3.10"            │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ FILTER 1: TestCodeGenerator (Pynguin Mode)                          │
│ Processing:                                                          │
│   • Parse source code AST                                            │
│   • Identify testable functions                                      │
│   • Run Pynguin WHOLE_SUITE algorithm                               │
│   • Generate 5 test cases                                            │
│   • Achieve 85% line coverage                                        │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PIPE 2: Generated Tests                                              │
│ Data: test_triangle.py with 5 test functions                        │
│ Metadata: method="pynguin", coverage=85%, tests=5                   │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ FILTER 2: TestSmellDetector (Multi-Agent Mode)                      │
│ Processing:                                                          │
│   • Parse test_triangle.py AST                                       │
│   • Agent 1 detects: 2 Assertion Roulettes                          │
│   • Agent 2 detects: 1 Magic Number Test                            │
│   • Agent 3 detects: 2 Assertion Roulettes, 1 Eager Test            │
│   • Consensus: 2 Assertion Roulettes, 1 Magic Number, 1 Eager Test  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PIPE 3: Smell Detection Report                                       │
│ Data: 4 smells detected in test_triangle.py                         │
│ Metadata: method="multi_agent", confidence_avg=0.87                 │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ FILTER 3: RefactoringEngine (Multi-Agent Mode)                      │
│ Processing:                                                          │
│   • Analyzer: Review 4 detected smells                               │
│   • Refactorer: Propose fixes (add assert messages, extract const)  │
│   • Reviewer: Validate proposals                                     │
│   • Validator: Execute tests, verify behavior preservation           │
│   • Apply: Transform code, all tests still pass                      │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PIPE 4: Refactored Code                                              │
│ Data: test_triangle_refactored.py (4 smells fixed)                  │
│ Metadata: method="multi_agent", validation="passed"                 │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ FILTER 4: ReportGenerator                                            │
│ Processing:                                                          │
│   • Aggregate metrics: 5 tests generated, 4 smells detected         │
│   • Calculate: Detection accuracy = 100%, Refactoring success = 100%│
│   • Generate visualization charts                                    │
│   • Format HTML report with code comparisons                         │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ OUTPUT: Comprehensive Report                                         │
│ Files:                                                               │
│   • triangle.py (original source)                                    │
│   • test_triangle.py (generated tests)                               │
│   • smell_report.html (detection results)                            │
│   • test_triangle_refactored.py (clean tests)                        │
│   • evaluation_report.html (full pipeline metrics)                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

#### Implementation Mapping

| Pipe/Filter Component | Python Class | Module Location |
|----------------------|--------------|-----------------|
| Filter 1 | TestCodeGenerator | `backend/modules/test_generator/` |
| Filter 2 | TestSmellDetector | `backend/modules/smell_detector/` |
| Filter 3 | RefactoringEngine | `backend/services/` |
| Filter 4 | ReportManager | `backend/services/` |
| Pipe Management | ArtifactLibraryManager | `backend/services/` |
| Pipeline Orchestration | Flask Routes | `backend/routes/` |

---

#### Alternative Pipeline Configurations

##### Configuration 1: Generation Only
```
Source Code → TestCodeGenerator → Output (Tests)
```
User receives generated tests without smell analysis.

##### Configuration 2: Detection Only
```
Existing Tests → TestSmellDetector → Output (Smell Report)
```
User analyzes existing test suite for smells.

##### Configuration 3: Generation + Detection
```
Source Code → TestCodeGenerator → TestSmellDetector → Output (Tests + Report)
```
User receives tests and smell analysis without refactoring.

##### Configuration 4: Full Pipeline (Default)
```
Source Code → TestCodeGenerator → TestSmellDetector → RefactoringEngine → ReportGenerator → Output
```
Complete automated testing workflow with all stages.

---

#### Extensibility Points

The Pipe and Filter architecture enables easy extension:

**Adding New Filters:**
- Pre-processing filter: Code formatting, style checking
- Post-refactoring filter: Test execution, mutation testing
- Analysis filter: Complexity metrics, duplication detection

**Adding New Pipes:**
- Cache pipe: Store intermediate results for reuse
- Validation pipe: Verify data integrity between filters
- Logging pipe: Track data transformations

**Alternative Filter Implementations:**
- Different LLM providers (Claude, Mistral)
- Different test generators (Hypothesis, pytest-randomly)
- Different detection tools (Pylint, Flake8 integration)

---

This Pipe and Filter architecture ensures PyTestGenie maintains a clean separation of concerns, enables flexible configuration, and provides a clear, maintainable structure for the automated testing pipeline.

---

### 6.7.2 Layered Architecture Instantiation

PyTestGenie implements a **Layered Architecture** that organizes the system into four hierarchical layers, where each layer provides services to the layer above it and consumes services from the layer below.

#### Layered Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LAYER 1: PRESENTATION LAYER                         │
│              (User Interface, API Endpoints, Request Handling)              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  • React Frontend (Login, Dashboard, TestGenerator, SmellDetector)          │
│  • REST API Endpoints (/api/auth, /api/test-generator, /api/smell-detector) │
│  • JWT Authentication & Request Validation                                  │
│  • JSON Response Formatting & Error Handling                                │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTP/REST (JSON)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LAYER 2: BUSINESS LOGIC LAYER                          │
│         (Core Processing, Services, Business Rules, External APIs)          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  • UserManager (Authentication, Authorization, Session Management)          │
│  • DashboardManager (Profile Management, User Preferences)                  │
│  • TestCodeGenerator (Pynguin Integration, LLM-based Generation)            │
│  • TestSmellDetector (Rule-based Detection, LLM Analysis, Multi-Agent)      │
│  • RefactoringEngine (Code Transformation, Multi-Agent Orchestration)       │
│  • LLMModelManager (Gemini/GPT/Llama Integration, Prompt Dispatching)       │
│  • ReportManager (Metrics Calculation, Report Generation, Export)           │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ Service Calls
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LAYER 3: PERSISTENCE LAYER                            │
│            (Data Access, Repository Pattern, Storage Management)            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  • UserRepository (User CRUD, Authentication Queries)                       │
│  • ProjectRepository (Project Management, File Organization)                │
│  • TestRepository (Generated Test Storage, Metadata Management)             │
│  • SmellReportRepository (Detection Report Storage, Statistics)             │
│  • RefactoringRepository (Refactored Code History, Validation)              │
│  • ArtifactLibraryManager (File Operations, Storage Quota, Versioning)      │
│  • SQLAlchemy ORM (Session Management, Transaction Control, Query Builder)  │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ SQL Queries / File I/O
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LAYER 4: DATA LAYER                                │
│                  (Physical Storage, Database, File System)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  • Database (PostgreSQL/SQLite)                                             │
│    - Tables: User, UserSettings, Project, SourceFile, GeneratedTest,       │
│              SmellDetectionReport, DetectedSmell, RefactoredCode,           │
│              EvaluationReport                                               │
│    - Relationships: Foreign Keys, Indexes, Constraints                      │
│                                                                             │
│  • File System Storage (uploads/)                                           │
│    - Directory Structure: user_{id}/projects/source_files/tests/reports/   │
│    - File Types: .py (source/tests), .html (reports), .json (data)         │
│    - Storage Management: User quotas, cleanup policies                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

#### Layer Details

##### Layer 1: Presentation Layer
**(User Interface, API Endpoints, Request Handling)**

**Components:**
- **React Frontend**: Login, Dashboard, AdminPanel, TestGenerator, SmellDetector components
- **REST API**: Flask routes for authentication, test generation, smell detection, refactoring, reports
- **Authentication**: JWT token validation, role-based access control
- **Communication**: HTTP/REST with JSON payloads

**Responsibilities:**
- Display user interfaces and collect user input
- Expose HTTP endpoints for frontend-backend communication
- Validate incoming requests and format responses
- Handle authentication and authorization at API gateway level

---

##### Layer 2: Business Logic Layer
**(Core Processing, Services, Business Rules, External APIs)**

**Components:**
- **UserManager**: User authentication, authorization, session management
- **DashboardManager**: User profile and preference management
- **TestCodeGenerator**: Test generation using Pynguin algorithms and LLM models
- **TestSmellDetector**: Multi-method smell detection (rule-based, LLM, multi-agent)
- **RefactoringEngine**: Code transformation with multi-agent workflows
- **LLMModelManager**: Integration with Gemini, GPT, Llama APIs
- **ReportManager**: Metrics aggregation, report generation, export formatting

**Responsibilities:**
- Execute core application logic and business rules
- Coordinate between different services and modules
- Interface with external LLM APIs for AI-powered features
- Enforce business constraints and validation rules
- Process data transformations through the testing pipeline

**Key Business Rules:**
- Admins must approve new user registrations
- Generated tests must achieve minimum 70% coverage
- Refactored code must preserve original test behavior
- Multi-agent detection requires 2+ agents consensus

---

##### Layer 3: Persistence Layer
**(Data Access, Repository Pattern, Storage Management)**

**Components:**
- **Repositories**: UserRepository, ProjectRepository, TestRepository, SmellReportRepository, RefactoringRepository
- **ArtifactLibraryManager**: File system operations, storage quota management, versioning
- **SQLAlchemy ORM**: Object-relational mapping, session management, transaction control

**Responsibilities:**
- Provide data access abstraction through repository pattern
- Manage database CRUD operations
- Handle file system storage and retrieval
- Enforce storage quotas and cleanup policies
- Map domain objects to database entities

**Data Operations:**
- Create, Read, Update, Delete for all entities
- Complex queries for reporting and statistics
- Transaction management for data integrity
- File upload/download and directory organization

---

##### Layer 4: Data Layer
**(Physical Storage, Database, File System)**

**Components:**

**Database (PostgreSQL/SQLite):**
- 9 tables: User, UserSettings, Project, SourceFile, GeneratedTest, SmellDetectionReport, DetectedSmell, RefactoredCode, EvaluationReport
- Relationships with foreign keys and cascade rules
- Indexes for query optimization
- ACID compliance for data integrity

**File System Storage:**
- Directory structure: `uploads/user_{id}/projects/source_files/tests/reports/`
- File types: `.py` (source/tests), `.html` (reports), `.json` (data), `.pdf` (exports)
- Storage quotas: 500 MB per user default
- Automatic cleanup of files older than 1 year

**Responsibilities:**
- Persistent storage of all application data
- Enforce referential integrity and constraints
- Store actual file content (code, reports, artifacts)
- Maintain directory structure for user isolation

---

#### Layer Communication Flow

**Top-Down Only** (Each layer only calls the layer directly below):

```
User Action
    ↓
Presentation Layer (React → API)
    ↓
Business Logic Layer (Services → Processing)
    ↓
Persistence Layer (Repositories → ORM)
    ↓
Data Layer (Database / File System)
```

**Example Flow: Generate Tests**
1. **Presentation**: User clicks "Generate" → POST `/api/test-generator/generate`
2. **Business Logic**: TestCodeGenerator processes source code → Executes Pynguin/LLM
3. **Persistence**: TestRepository saves metadata → ArtifactLibraryManager stores file
4. **Data**: INSERT into database → Write file to `uploads/` directory

---

#### Benefits

**1. Separation of Concerns**: Each layer has distinct responsibilities  
**2. Technology Independence**: Can swap implementations without affecting other layers  
**3. Testability**: Layers can be tested independently with mocks  
**4. Maintainability**: Changes isolated to specific layers  
**5. Scalability**: Layers can be scaled independently  
**6. Security**: Multiple security checkpoints across layers  

---

#### Technology Stack by Layer

| Layer | Technologies |
|-------|-------------|
| Presentation | React, Vite, Axios, Flask, Flask-CORS, JWT |
| Business Logic | Python, Pynguin, LLM APIs (Gemini, GPT, Llama) |
| Persistence | SQLAlchemy, Repository Pattern, File I/O |
| Data | PostgreSQL/SQLite, File System |

---

This Layered Architecture ensures PyTestGenie maintains clear separation of concerns, with each layer focused on specific responsibilities, enabling maintainability, scalability, and independent evolution of system components.

---

## 7. Preliminary Test Plan

This chapter presents a high-level description of testing goals and a comprehensive summary of features to be tested for the PyTestGenie system.

### 7.1 High Level Description of Testing Goals

The primary testing goals for the PyTestGenie system are as follows:

- **To validate that PyTestGenie meets its functional and non-functional requirements** for automated Python unit test generation, smell detection, and refactoring.

- **To ensure accurate test generation** using both search-based (Pynguin) and AI-powered (LLM) approaches with minimum 70% code coverage.

- **To verify that test smell detection mechanisms** (rule-based, LLM-based, and multi-agent) identify code smells accurately with appropriate confidence thresholds.

- **To confirm that the refactoring engine** preserves test behavior while eliminating detected smells through automated code transformations.

- **To validate the AI model integration** (Gemini, GPT, Llama) processes prompts correctly and returns valid, contextually accurate responses.

- **To test user authentication and role-based access control** ensuring admin and regular users have appropriate permissions.

- **To ensure the artifact library management** handles file uploads, storage quotas, and directory organization correctly.

- **To test report generation** for comprehensive metrics, visualizations, and export capabilities (HTML, PDF, JSON).

- **To verify system performance and scalability** under concurrent user operations and high-load scenarios.

- **To confirm the usability and accessibility** of the interface across different browsers and platforms.

- **To validate integration with external services** (LLM APIs, Pynguin, email SMTP) handles failures gracefully with appropriate fallback mechanisms.

---

### 7.2 Test Cases

Below is a comprehensive set of test cases designed to evaluate PyTestGenie thoroughly across all functional and non-functional requirements.

---

#### Test Case 1

**User Registration and Authentication**

**Test Scenario:** A new user registers an account and logs into the PyTestGenie system.

**Steps:**
1. Register a new account with valid credentials (username, email, password).
2. Verify email confirmation is sent.
3. Admin approves the pending registration.
4. User logs in using registered credentials.

**Expected Outcome:**
- User account is created with "pending" status.
- Email confirmation is sent to the user's email address.
- Admin can view and approve pending users.
- After approval, user status changes to "active".
- User successfully logs in and accesses the personalized dashboard.
- JWT token is generated and stored for session management.

---

#### Test Case 2

**Admin User Management**

**Test Scenario:** Admin user manages user accounts (approve, deactivate, delete).

**Steps:**
1. Admin logs into the system.
2. Admin views list of pending user registrations.
3. Admin approves a pending user.
4. Admin deactivates an active user.
5. Admin deletes a user account.

**Expected Outcome:**
- Admin successfully views all users with their statuses.
- Approved users can log in and access the system.
- Deactivated users cannot log in (receive authentication error).
- Deleted users are removed from the database with cascade deletion of all related data.
- Email notifications are sent for status changes.

---

#### Test Case 3.1

**Test Generation Using Pynguin (Search-Based)**

**Test Scenario:** User generates unit tests for Python source code using Pynguin.

**Steps:**
1. User uploads a valid Python source file (e.g., `triangle.py`).
2. User selects "Pynguin" as the generation method.
3. User configures algorithm (e.g., DYNAMOSA) and budget (60 seconds).
4. User initiates test generation.
5. User views real-time streaming logs.

**Expected Outcome:**
- Source file is uploaded and validated successfully.
- Pynguin executes with selected algorithm and budget.
- Real-time logs are streamed to the frontend.
- Generated test file is created with valid Python syntax.
- Coverage metrics are calculated and displayed (target: ≥70%).
- Generated test is saved to database and file system.
- User can download the generated test file.

---

#### Test Case 3.2

**Test Generation Using LLM (AI-Powered)**

**Test Scenario:** User generates unit tests using an LLM model (Gemini/GPT/Llama).

**Steps:**
1. User uploads a valid Python source file.
2. User selects "LLM" as the generation method.
3. User selects an LLM model (e.g., Gemini).
4. User initiates test generation.

**Expected Outcome:**
- LLM API is called with properly formatted prompt.
- Generated test code follows pytest conventions.
- Test includes assertions, edge cases, and documentation.
- Coverage metrics are estimated or calculated.
- Generated test is syntactically valid Python code.
- Results are saved and displayed to the user.

---

#### Test Case 3.3

**Invalid Source Code Upload Handling**

**Test Scenario:** User attempts to upload an invalid or malformed Python file.

**Steps:**
1. User attempts to upload a file with syntax errors.
2. User attempts to upload a non-Python file (e.g., `.txt`, `.jpg`).

**Expected Outcome:**
- System rejects files with invalid extensions.
- Error message indicates the file format is unsupported.
- For Python files with syntax errors, system provides specific error details.
- No partial or corrupted data is saved to the database.

---

#### Test Case 4.1

**Rule-Based Test Smell Detection**

**Test Scenario:** User analyzes a test file for smells using rule-based detection.

**Steps:**
1. User uploads or selects a generated test file.
2. User selects "Rule-Based" detection method.
3. User initiates smell detection analysis.

**Expected Outcome:**
- System parses test file AST successfully.
- TeMPy detection rules are applied.
- Detected smells include: Assertion Roulette, Eager Test, Lazy Test, Mystery Guest, etc.
- Each smell includes: name, severity, location (line numbers), description.
- Detection report is generated with summary statistics.
- Confidence score is set to 1.0 for rule-based detection.

---

#### Test Case 4.2

**LLM-Based Test Smell Detection**

**Test Scenario:** User analyzes a test file using LLM-powered smell detection.

**Steps:**
1. User uploads a test file.
2. User selects "LLM-Based" detection method.
3. User selects an LLM model (e.g., GPT-4).
4. User initiates analysis.

**Expected Outcome:**
- Test code is sent to LLM with detection prompt.
- LLM identifies smells with explanations.
- Results include smell type, location, reasoning, and refactoring suggestions.
- Confidence score reflects LLM's certainty (0.60 - 1.0).
- Results are parsed and stored in structured format.

---

#### Test Case 4.3

**Multi-Agent Test Smell Detection**

**Test Scenario:** User uses multiple agents (rule-based + multiple LLMs) for consensus-based detection.

**Steps:**
1. User uploads a test file.
2. User selects "Multi-Agent" detection method.
3. System configures 3+ agents (e.g., Rule-Based, Gemini, GPT).
4. User initiates analysis.

**Expected Outcome:**
- All configured agents analyze the test file independently.
- System aggregates results from all agents.
- Consensus algorithm determines final smell detection (requires 2+ agents agreement).
- Final report includes: smell name, confidence (average), voting details, per-agent results.
- User can view individual agent outputs.

---

#### Test Case 5

**Smell Refactoring with Behavior Preservation**

**Test Scenario:** User refactors detected smells while preserving test behavior.

**Steps:**
1. User views smell detection report.
2. User selects a detected smell for refactoring.
3. System applies appropriate refactoring pattern.
4. User reviews refactored code.
5. System validates behavior preservation.

**Expected Outcome:**
- Refactoring engine applies correct transformation (e.g., split Eager Test into multiple tests).
- Refactored code is syntactically valid Python.
- Original test file is backed up before modification.
- Validation tests confirm behavior is preserved (all assertions pass).
- Refactoring explanation is generated for user understanding.
- Success/failure status is recorded.

---

#### Test Case 6

**Report Generation and Export**

**Test Scenario:** User generates comprehensive reports and exports in multiple formats.

**Steps:**
1. User completes the full pipeline (generation → detection → refactoring).
2. User requests a comprehensive evaluation report.
3. User exports report in HTML format.
4. User exports report in JSON format.
5. User exports report in PDF format.

**Expected Outcome:**
- Report includes all pipeline stages with metrics.
- Metrics include: coverage %, smell count by type, refactoring success rate, execution time.
- HTML report contains visualizations (charts, tables) and is viewable in browser.
- JSON report is valid JSON with structured data.
- PDF report is properly formatted with all sections.
- All export formats contain consistent data.

---

#### Test Case 7

**User Library Management**

**Test Scenario:** User manages personal artifact library (source files, tests, reports).

**Steps:**
1. User uploads multiple source files to the library.
2. User organizes files into projects.
3. User searches for artifacts by name or project.
4. User downloads artifacts from the library.
5. User deletes old artifacts.

**Expected Outcome:**
- Files are stored in user-specific directory (`uploads/user_{id}/`).
- Storage quota is enforced (500 MB default per user).
- Files are organized by projects and types.
- Search returns matching results.
- Download provides correct file content.
- Deletion removes file from both database and file system.
- Automatic cleanup removes files older than 1 year.

---

#### Test Case 8

**Performance Under High Load**

**Test Scenario:** Testing system performance when multiple users perform operations simultaneously.

**Steps:**
1. Simulate 20 concurrent users uploading source files.
2. Simulate 15 users generating tests with Pynguin simultaneously.
3. Simulate 10 users running LLM-based smell detection concurrently.
4. Monitor response times and system resources.

**Expected Outcome:**
- System handles concurrent requests without crashes.
- Response times remain acceptable (< 5 seconds for API calls, excluding generation/detection time).
- Database connections are properly pooled and managed.
- File system operations do not conflict.
- All users receive their results successfully without data corruption.
- System logs concurrent operations properly.

---

#### Test Case 9

**LLM API Integration and Fallback**

**Test Scenario:** Testing LLM service integration and fallback mechanisms.

**Steps:**
1. User initiates LLM-based test generation with Gemini.
2. Simulate Gemini API failure.
3. System attempts fallback to GPT.
4. Simulate GPT API failure.
5. System attempts fallback to Llama.

**Expected Outcome:**
- System successfully calls Gemini API when available.
- When Gemini fails, system automatically tries GPT without user intervention.
- When GPT fails, system tries Llama.
- User is notified of which model is being used.
- If all models fail, user receives clear error message.
- Error is logged for debugging.
- System handles API rate limiting gracefully.

---

#### Test Case 10.1

**Validation with Similar Source Code for Consistent Test Generation**

**Test Scenario:** Generate tests for similar functions to validate consistency.

**Steps:**
1. For five similar mathematical functions (e.g., `add`, `subtract`, `multiply`, `divide`, `modulo`), generate tests using Pynguin.
2. Compare the test structures, coverage, and patterns.

**Expected Outcome:**
- Similar functions produce tests with similar structures.
- All tests achieve target coverage (≥70%).
- Test generation times are comparable.
- Validates that Pynguin algorithms work consistently for similar code patterns.

---

#### Test Case 10.2

**Validation with Different Complexity Levels**

**Test Scenario:** Generate tests for functions with varying complexity to validate adaptability.

**Steps:**
1. Generate tests for simple function (e.g., `max(a, b)`).
2. Generate tests for medium complexity (e.g., `binary_search`).
3. Generate tests for high complexity (e.g., `quicksort`).
4. Compare coverage, test count, and generation time.

**Expected Outcome:**
- Simple functions achieve high coverage (>90%) quickly.
- Medium complexity achieves target coverage (70-85%).
- High complexity may require extended budget but still achieves reasonable coverage.
- Validates that system adapts to different complexity levels.

---

#### Test Case 10.3

**Cross-Validation Between Generation Methods**

**Test Scenario:** Compare Pynguin-generated and LLM-generated tests for the same source code.

**Steps:**
1. Generate tests for `triangle_validator.py` using Pynguin.
2. Generate tests for same file using LLM (Gemini).
3. Compare coverage, test quality, and smell detection results.

**Expected Outcome:**
- Both methods produce valid, executable tests.
- Coverage metrics are comparable (within 10% difference).
- LLM tests may have better readability and documentation.
- Pynguin tests may achieve higher branch coverage.
- Validates that both methods are viable for test generation.

---

#### Test Case 11

**Smell Detection Consistency Across Methods**

**Test Scenario:** Verify that different detection methods identify smells appropriately.

**Steps:**
1. Analyze a test file known to contain "Assertion Roulette" using rule-based detection.
2. Analyze the same file using LLM-based detection.
3. Analyze using multi-agent detection.
4. Compare results across all three methods.

**Expected Outcome:**
- Rule-based detection identifies "Assertion Roulette" with 100% confidence.
- LLM-based detection identifies the same smell with explanation.
- Multi-agent detection reaches consensus on the smell.
- All methods agree on the presence of the smell.
- Validates detection accuracy and consistency.

---

#### Test Case 12

**Validation Against Known Benchmarks**

**Test Scenario:** Test PyTestGenie against known benchmark datasets.

**Steps:**
1. Use test files from TeMPy dataset containing known smells.
2. Run rule-based detection on benchmark files.
3. Compare detected smells with ground truth annotations.
4. Calculate precision and recall metrics.

**Expected Outcome:**
- Detection precision ≥ 85% (few false positives).
- Detection recall ≥ 80% (most true positives detected).
- System identifies all documented smells in benchmark.
- Validates that detection algorithms meet academic standards.

---

#### Test Case 13

**Refactoring Customization and Validation**

**Test Scenario:** Test that refactoring respects user preferences and validates correctly.

**Steps:**
1. Detect "Eager Test" smell in a test file.
2. User selects refactoring option with preference for minimal changes.
3. Apply refactoring.
4. Run validation tests.
5. Repeat with preference for aggressive refactoring.

**Expected Outcome:**
- Minimal refactoring splits test into 2-3 smaller tests.
- Aggressive refactoring may split into individual test methods per assertion.
- Both refactored versions pass all original test assertions.
- Behavior preservation validation succeeds.
- Refactoring respects user's customization preferences.

---

#### Test Case 14

**Email Notification System**

**Test Scenario:** Verify that email notifications are sent for key events.

**Steps:**
1. New user registers (pending approval).
2. Admin approves user registration.
3. User completes a test generation task.
4. Long-running analysis completes.

**Expected Outcome:**
- Admin receives email notification of new pending user.
- User receives confirmation email upon approval.
- User receives notification when test generation completes (for long tasks).
- All emails contain relevant information and links.
- Email delivery failures are logged but do not block system operations.

---

#### Test Case 15

**Database Integrity and Cascade Operations**

**Test Scenario:** Verify database relationships and cascade deletions work correctly.

**Steps:**
1. User creates a project with source files.
2. Generate tests for source files.
3. Run smell detection on generated tests.
4. Apply refactoring.
5. Delete the user account.

**Expected Outcome:**
- All related records are created with proper foreign keys.
- When user is deleted:
  - All projects are deleted (cascade).
  - All source files are deleted (cascade).
  - All generated tests are deleted (cascade).
  - All smell reports are deleted (cascade).
  - All refactored code versions are deleted (cascade).
- File system artifacts are cleaned up.
- No orphaned records remain in database.

---

#### Test Case 16

**Multi-Browser and Cross-Platform Compatibility**

**Test Scenario:** Verify frontend works across different browsers and platforms.

**Steps:**
1. Access PyTestGenie from Chrome, Firefox, Edge, Safari.
2. Test on Windows, macOS, Linux.
3. Perform key operations: login, test generation, smell detection, report viewing.

**Expected Outcome:**
- UI renders correctly in all browsers.
- All features function properly across browsers.
- Responsive design adapts to different screen sizes.
- No JavaScript errors in any browser console.
- File upload/download works on all platforms.

---

#### Test Case 17

**Storage Quota Enforcement**

**Test Scenario:** Verify that user storage quotas are enforced properly.

**Steps:**
1. User uploads files totaling 450 MB (under 500 MB quota).
2. User attempts to upload additional 100 MB file (exceeds quota).
3. Admin increases user's quota to 1 GB.
4. User successfully uploads the 100 MB file.

**Expected Outcome:**
- First upload succeeds, storage usage is tracked correctly.
- Second upload is rejected with quota exceeded error.
- After quota increase, upload succeeds.
- Storage calculation includes all user artifacts.
- Old files can be deleted to free up space.

---

#### Test Case 18

**Concurrent Multi-Agent Detection**

**Test Scenario:** Verify multi-agent detection handles concurrent agent execution properly.

**Steps:**
1. Configure multi-agent with 5 agents (Rule, Gemini, GPT, Llama, HuggingFace).
2. Initiate detection on a large test file.
3. Monitor that all agents execute in parallel.

**Expected Outcome:**
- All 5 agents start execution simultaneously or near-simultaneously.
- Total execution time is approximately equal to the slowest agent (not sum of all).
- Results from all agents are collected successfully.
- Consensus algorithm processes all agent outputs correctly.
- System handles if one agent fails without blocking others.

---

This comprehensive test plan ensures PyTestGenie is validated across all functional areas, performance requirements, integration points, and edge cases, providing confidence in the system's reliability and correctness.

---

## Overview
PyTestGenie is a unified platform combining automated test generation and test smell detection for Python projects.

## Architecture

### Backend (Flask API)
```
backend/
├── app_unified.py              # Main Flask application
├── config/
│   └── settings.py            # Configuration management
├── routes/
│   ├── test_generation.py     # /api/test-generator endpoints
│   └── smell_detection.py     # /api/smell-detector endpoints
├── modules/
│   ├── test_generator/        # Test generation logic
│   └── smell_detector/        # Smell detection logic
```

### Frontend (React)
```
frontend/src/
├── App.jsx                    # Main application with tab navigation
├── components/
│   ├── TestGenerator.jsx     # Test generation UI
│   └── SmellDetector.jsx     # Smell detection UI
```

## Module Responsibilities

### Test Generator Module
- **pynguin_generator.py**: Interfaces with Pynguin for automatic test generation
- **ai_generator.py**: Uses OpenAI API (via HuggingFace) for AI-powered test generation
- **models.py**: Data models for test generation results

### Smell Detector Module
- **analyzer.py**: Main coordinator for smell detection
- **detector.py**: Smell detection algorithms
- **python_parser.py**: Parses Python test files
- **report_generator.py**: Generates HTML reports

## API Endpoints

### Test Generation
- `POST /api/test-generator/generate-tests/pynguin` - Generate using Pynguin
- `GET /api/test-generator/generate-tests/stream/<task_id>` - Stream Pynguin logs
- `POST /api/test-generator/generate-tests/ai` - Generate using AI

### Smell Detection
- `POST /api/smell-detector/analyze/code` - Analyze code string
- `POST /api/smell-detector/analyze/file` - Analyze uploaded file
- `POST /api/smell-detector/analyze/directory` - Analyze multiple files
- `POST /api/smell-detector/analyze/github` - Analyze GitHub repo
- `GET /api/smell-detector/report` - Get HTML report

## Data Flow

### Test Generation Flow
1. User enters code in frontend
2. Frontend sends POST to backend API
3. Backend invokes appropriate generator (Pynguin/AI)
4. Results streamed (Pynguin) or returned directly (AI)
5. Frontend displays generated tests
6. User can trigger smell detection on generated tests

### Smell Detection Flow
1. User provides code/file/directory/GitHub URL
2. Frontend sends to backend API
3. Backend:
   - Saves/clones files if needed
   - Runs analyzer on test files
   - Generates HTML report
4. Frontend displays results summary
5. User can view detailed HTML report

## File Responsibilities

### Backend Files

**app_unified.py**
- Application factory
- Blueprint registration
- CORS configuration
- Root endpoints

**config/settings.py**
- Environment configuration
- Flask settings
- API tokens

**routes/test_generation.py**
- Test generation endpoints
- Task queue management for Pynguin
- SSE streaming for logs

**routes/smell_detection.py**
- Smell detection endpoints
- File upload handling
- GitHub integration
- Report serving

**modules/test_generator/pynguin_generator.py**
- Pynguin command execution
- Log streaming
- Async task management

**modules/test_generator/ai_generator.py**
- OpenAI API integration
- Prompt engineering
- Response parsing

**modules/smell_detector/analyzer.py**
- File analysis coordination
- Report generation
- Test file detection

### Frontend Files

**App.jsx**
- Tab navigation (Generator/Detector)
- Component routing
- Application layout

**components/TestGenerator.jsx**
- Method selection (Pynguin/AI)
- Code input
- Generation triggering
- Result display
- Smell detection integration

**components/SmellDetector.jsx**
- Mode selection (Code/File/Directory/GitHub)
- Input handling
- Analysis triggering
- Result display

## Configuration

### Environment Variables
- `HF_TOKEN`: HuggingFace API token for AI generation
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Environment (development/production)
- `CORS_ORIGINS`: Allowed CORS origins

### Settings Classes
- `Config`: Base configuration
- `DevelopmentConfig`: Development settings
- `ProductionConfig`: Production settings

## Error Handling

### Backend
- Try-catch blocks in all endpoints
- Meaningful error messages
- HTTP status codes
- Error logging

### Frontend
- axios error handling
- User-friendly alerts
- Loading states
- Validation

## Security Considerations

1. **File Uploads**: Secure filename sanitization
2. **CORS**: Configured origins only
3. **API Tokens**: Environment variables only
4. **Temporary Files**: Cleaned up after use
5. **Input Validation**: All inputs validated

## Performance Optimizations

1. **Streaming**: SSE for Pynguin logs
2. **Async**: Background tasks for long operations
3. **Cleanup**: Temporary files removed immediately
4. **Caching**: Static files cached

## Deployment Notes

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python app_unified.py
```

### Frontend Deployment
```bash
cd frontend
npm install
npm run build
npm run preview
```

### Production Considerations
- Use production WSGI server (gunicorn/uwsgi)
- Set FLASK_ENV=production
- Configure proper CORS origins
- Use environment-specific .env files
- Enable HTTPS
- Set up proper logging

## Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## Maintenance

### Adding New Features
1. Create module in `backend/modules/`
2. Create routes in `backend/routes/`
3. Register blueprint in `app_unified.py`
4. Create React component in `frontend/src/components/`
5. Update App.jsx navigation

### Updating Dependencies
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

## Troubleshooting Guide

### Common Issues

**Backend won't start**
- Check .env file exists
- Verify Python dependencies installed
- Check port 5000 availability

**Frontend won't start**
- Run `npm install`
- Check Node.js version >= 14
- Verify port 3000 availability

**CORS errors**
- Check CORS_ORIGINS in .env
- Verify backend is running
- Check API_BASE URLs in frontend

**Generation fails**
- Verify HF_TOKEN in .env
- Check code is valid Python
- Review backend logs

## Future Enhancements

1. User authentication
2. Test history/storage
3. Custom smell detection rules
4. Batch processing
5. Export to different formats
6. Integration with CI/CD
7. Performance metrics
8. Test coverage analysis
