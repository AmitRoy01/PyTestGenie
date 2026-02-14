# Class-Based Modeling - PyTestGenie

## Overview

Class-based modeling is a technique in software engineering used to represent the structure of a system through classes, their attributes, methods, and the relationships between them. It is a key part of object-oriented design, helping developers visualize how different components of the system are organized and interact.

For PyTestGenie, class-based modeling defines the structural backbone of the automated testing pipeline, from user management through test generation, smell detection, refactoring, and report generation.

---

## 5.1 Analysis Classes

To define the structural backbone of PyTestGenie, I performed a noun-extraction analysis on the project requirements. Starting with 52 potential nouns, I filtered for those representing unique state and behavior within the testing pipeline. 

Using the **Selection Criteria**:
- **Retained information**: Classes that maintain state across operations
- **Needed services**: Classes providing essential system functionality
- **Multiple attributes**: Classes with multiple related properties
- **Common attributes**: Classes sharing related data structures
- **Common operations**: Classes with cohesive method sets
- **Essential requirements**: Classes mapped directly to core requirements

I consolidated the system into **8 primary analysis classes**. These classes encapsulate everything from user management to the complex agentic logic required for LLM-based refactoring.

### The Selected 8 Classes:

1. **UserManager**: Handles the secure authentication and role-based access for the platform
2. **DashboardManager**: Manages user profiles
3. **TestCodeGenerator**: Coordinates the creation of initial test suites using rule-based or LLM-based generation
4. **TestSmellDetector**: Executes the dual-path detection (rule-based static analysis and agentic LLM analysis)
5. **RefactoringEngine**: Orchestrates the multi-agent workflow to transform smelly tests into high-quality code
6. **LLMModelManager**: Serves as the interface for various LLM providers (GPT, Gemini, etc.) and manages prompt dispatching
7. **ReportManager**: Aggregates data to generate reports
8. **ArtifactLibraryManager**: Saves or deletes files, code snippets, folders, and generated reports

---

## 5.2 Class Relationship Diagram

```
┌──────────────────┐
│  UserManager     │
└────────┬─────────┘
         │
         │ manages
         ▼
┌──────────────────────┐         ┌──────────────────────────┐
│ DashboardManager     │◄───────►│ ArtifactLibraryManager   │
└──────────┬───────────┘         └────────┬─────────────────┘
           │                              │
           │ configures                   │ provides artifacts
           ▼                              │
┌──────────────────────┐         ┌───────▼──────────────────┐
│ TestCodeGenerator    │◄───────►│   LLMModelManager        │
└──────────┬───────────┘         └───────┬──────────────────┘
           │                              │
           │ produces tests               │ uses
           ▼                              │
┌──────────────────────┐                 │
│ TestSmellDetector    │◄────────────────┘
└──────────┬───────────┘
           │
           │ detects smells
           ▼
┌──────────────────────┐         ┌──────────────────────┐
│  RefactoringEngine   │◄───────►│  LLMModelManager     │
└──────────┬───────────┘         └──────────────────────┘
           │
           │ provides results
           ▼
┌──────────────────────┐
│   ReportManager      │
└──────────────────────┘
```

---

## 5.3 CRC Cards

### Table-1: CRC Card (UserManager)

| **UserManager** | |
|----------|---------|
| **Attributes** | **Methods** |
| - user_session<br>- user_roles<br>- credentials_hash | + authenticate_user()<br>+ authorize_access()<br>+ update_credentials() |
| **Responsibilities** | **Collaborators** |
| Validates credentials and manages account registration.<br>Ensures only Admins can verify new user registrations. | DashboardManager |

---

### Table-2: CRC Card (DashboardManager)

| **DashboardManager** | |
|----------|---------|
| **Attributes** | **Methods** |
| - user_name<br>- user_role | + load_dashboard()<br>+ update_profile() |
| **Responsibilities** | **Collaborators** |
| Manages user profile. | UserManager |

---

### Table-3: CRC Card (TestCodeGenerator)

| **TestCodeGenerator** | |
|----------|---------|
| **Attributes** | **Methods** |
| - code_generation_method<br>- llm_model<br>- test_generator_algorithm<br>- code_context | + generate_test_code()<br>+ display_test_code()<br>+ compare_test_code() |
| **Responsibilities** | **Collaborators** |
| Generates unit tests using LLM or rule-based methods and presents multiple versions for user inspection. | DashboardManager,<br>LLMModelManager |

---

### Table-4: CRC Card (TestSmellDetector)

| **TestSmellDetector** | |
|----------|---------|
| **Attributes** | **Methods** |
| - detector_type<br>- code_snippet | + analyze_test_code()<br>+ detect_smells()<br>+ generate_smell_report() |
| **Responsibilities** | **Collaborators** |
| Identifies test smells in generated test code using TEMPY rules or LLM analysis. | TestCodeGenerator,<br>RefactoringEngine |

---

### Table-5: CRC Card (RefactoringEngine)

| **RefactoringEngine** | |
|----------|---------|
| **Attributes** | **Methods** |
| - agents_list<br>- feedback_loops<br>- refactored_code | + detect_and_confirm_smells()<br>+ refactor_test_code()<br>+ validate_refactoring() |
| **Responsibilities** | **Collaborators** |
| Coordinates multiple LLM agents to detect, confirm, and refactor test smells while ensuring correctness. | TestSmellDetector |

---

### Table-6: CRC Card (LLMModelManager)

| **LLMModelManager** | |
|----------|---------|
| **Attributes** | **Methods** |
| - available_models<br>- prompt_templates | + dispatch_prompt()<br>+ select_model()<br>+ parse_response() |
| **Responsibilities** | **Collaborators** |
| Connects the system to specific LLMs.<br>Formats chain-of-thought prompts for different agent roles. | TestSmellDetector,<br>RefactoringEngine |

---

### Table-7: CRC Card (ReportManager)

| **ReportManager** | |
|----------|---------|
| **Attributes** | **Methods** |
| - report_data<br>- design_data<br>- metrics_log | + generate_report()<br>+ calculate_metrics()<br>+ compile_results()<br>+ export_report() |
| **Responsibilities** | **Collaborators** |
| Creates exportable reports for developers and researchers from test generation, smell detection, and refactoring. | TestCodeGenerator,<br>TestSmellDetector,<br>RefactoringEngine |

---

### Table-8: CRC Card (ArtifactLibraryManager)

| **ArtifactLibraryManager** | |
|----------|---------|
| **Attributes** | **Methods** |
| - user_id<br>- artifact_list<br>- storage_path | + save_artifact()<br>+ get_artifact_history()<br>+ fetch_artifact_context()<br>+ delete_artifact() |
| **Responsibilities** | **Collaborators** |
| Stores uploaded Python code and generated files (code, reports).<br>Provides the code to the Detection/Refactoring engines. | TestCodeGenerator,<br>TestSmellDetector,<br>RefactoringEngine |

---

## 5.4 Class Interaction Scenarios

### Scenario 1: Test Generation Workflow

```
User → ProjectManager: upload_source_file(code)
ProjectManager → UserLibrary: store_source_file(code)
User → TestGenerator: generate_tests(method='llm')
TestGenerator → LLMServiceManager: select_model('gemini')
TestGenerator → LLMServiceManager: dispatch_prompt(generation_prompt)
LLMServiceManager → TestGenerator: return generated_tests
TestGenerator → UserLibrary: store_generated_tests(tests)
TestGenerator → User: display_tests(tests, coverage)
```

### Scenario 2: Smell Detection Workflow

```
User → SmellDetector: detect_smells(test_code, method='multi_agent')
SmellDetector → LLMServiceManager: dispatch_prompt(detection_prompt, agent_1)
SmellDetector → LLMServiceManager: dispatch_prompt(detection_prompt, agent_2)
SmellDetector → LLMServiceManager: dispatch_prompt(detection_prompt, agent_3)
SmellDetector: aggregate_results()
SmellDetector: classify_smells()
SmellDetector → UserLibrary: store_detection_report(report)
SmellDetector → User: display_smell_report(detected_smells)
```

### Scenario 3: Refactoring Workflow

```
User → CodeRefactorer: refactor_code(detected_smells, method='multi_agent')
CodeRefactorer: assign_agent_roles()
CodeRefactorer → LLMServiceManager: dispatch_prompt(analyze_prompt, analyzer_agent)
CodeRefactorer → LLMServiceManager: dispatch_prompt(refactor_prompt, refactorer_agent)
CodeRefactorer → LLMServiceManager: dispatch_prompt(review_prompt, reviewer_agent)
CodeRefactorer: select_best_refactoring()
CodeRefactorer: validate_refactoring()
CodeRefactorer → UserLibrary: store_refactored_code(code)
CodeRefactorer → User: display_comparison(original, refactored)
```

### Scenario 4: Report Generation Workflow

```
User → ReportGenerator: generate_report(project_id, type='full_pipeline')
ReportGenerator → TestGenerator: collect_generation_metrics()
ReportGenerator → SmellDetector: collect_detection_metrics()
ReportGenerator → CodeRefactorer: collect_refactoring_metrics()
ReportGenerator: calculate_accuracy()
ReportGenerator: calculate_success_rates()
ReportGenerator: create_visualizations()
ReportGenerator → UserLibrary: store_report(report)
ReportGenerator → User: export_report(format='html')
```

---

## 5.5 Design Patterns Applied

### 1. Strategy Pattern
**Classes**: TestGenerator, SmellDetector, CodeRefactorer  
**Purpose**: Allows switching between different algorithms (Pynguin algorithms, LLM models, detection methods) at runtime.

### 2. Facade Pattern
**Class**: LLMServiceManager  
**Purpose**: Provides a simplified interface to complex LLM API interactions across multiple providers.

### 3. Repository Pattern
**Class**: UserLibrary  
**Purpose**: Abstracts data persistence logic, providing a clean interface for storing and retrieving artifacts.

### 4. Factory Pattern
**Class**: ReportGenerator  
**Purpose**: Creates different types of reports (detection, refactoring, comparative) based on user requirements.

### 5. Observer Pattern
**Classes**: TestGenerator, SmellDetector, CodeRefactorer  
**Purpose**: Notifies ReportGenerator when pipeline stages complete to aggregate metrics.

---

## 5.6 Class Dependencies

### High-Level Dependencies

```
User
  └── ProjectManager
        ├── TestGenerator
        │     ├── LLMServiceManager
        │     └── SmellDetector
        │           ├── LLMServiceManager
        │           └── CodeRefactorer
        │                 ├── LLMServiceManager
        │                 └── ReportGenerator
        └── UserLibrary
```

### Dependency Principles Followed

1. **Dependency Inversion**: High-level modules (TestGenerator) depend on abstractions (LLMServiceManager interface) rather than concrete implementations.

2. **Single Responsibility**: Each class has one clear responsibility (e.g., SmellDetector only detects smells, doesn't refactor).

3. **Interface Segregation**: LLMServiceManager provides specific methods for different use cases (generation, detection, refactoring prompts).

4. **Low Coupling**: Classes interact through well-defined interfaces, minimizing direct dependencies.

---

## 5.7 Key Attributes and Methods Summary

### Attributes Summary

| Class | Key Attributes | Purpose |
|-------|---------------|---------|
| User | username, email, role, status | Identity and access control |
| ProjectManager | projects_list, source_files | File organization |
| TestGenerator | generation_method, llm_model, algorithm_type | Generation configuration |
| SmellDetector | detection_method, rule_engine, confidence_scores | Detection configuration |
| CodeRefactorer | refactoring_method, agent_roles, validation_status | Refactoring state |
| LLMServiceManager | available_models, prompt_templates, response_cache | LLM integration |
| ReportGenerator | report_type, metrics, statistics | Report data |
| UserLibrary | stored_artifacts, file_metadata, version_history | Artifact storage |

### Methods Summary

| Class | Key Methods | Purpose |
|-------|-------------|---------|
| User | authenticate(), authorize() | Access control |
| ProjectManager | create_project(), upload_source_file() | Project management |
| TestGenerator | generate_pynguin_tests(), generate_llm_tests() | Test generation |
| SmellDetector | detect_rule_based(), detect_multi_agent() | Smell detection |
| CodeRefactorer | refactor_multi_agent(), validate_refactoring() | Code refactoring |
| LLMServiceManager | dispatch_prompt(), parse_response() | LLM communication |
| ReportGenerator | calculate_accuracy(), export_html() | Report creation |
| UserLibrary | store_artifact(), retrieve_artifact() | Data persistence |

---

## 5.8 Class Implementation Technologies

| Class | Primary Technology | Framework/Library |
|-------|-------------------|-------------------|
| User | Python | SQLAlchemy Model |
| ProjectManager | Python | Flask Route Handler |
| TestGenerator | Python | Pynguin + LLM APIs |
| SmellDetector | Python | AST + LLM APIs |
| CodeRefactorer | Python | LLM APIs |
| LLMServiceManager | Python | google-generativeai, openai |
| ReportGenerator | Python | Jinja2, Matplotlib |
| UserLibrary | Python | SQLAlchemy + File System |

---

## 5.9 Class Design Rationale

The 8 analysis classes represent a carefully balanced architecture that:

1. **Separates Concerns**: Each class has a distinct, well-defined responsibility
   - **UserManager** handles authentication separately from user preferences
   - **DashboardManager** focuses solely on profile management
   - **LLMModelManager** provides a unified interface to all LLM providers

2. **Enables Flexibility**: 
   - **TestCodeGenerator** supports both rule-based (Pynguin) and LLM-based generation
   - **TestSmellDetector** implements multiple detection strategies
   - **RefactoringEngine** orchestrates complex multi-agent workflows

3. **Maintains Cohesion**:
   - **ArtifactLibraryManager** centralizes all storage operations
   - **ReportManager** aggregates metrics from all pipeline stages
   - Each class collaborates through well-defined interfaces

4. **Supports Extensibility**:
   - New LLM models can be added to **LLMModelManager** without affecting other classes
   - Additional detection methods can be integrated into **TestSmellDetector**
   - New report formats can be added to **ReportManager**

This design ensures PyTestGenie remains maintainable, testable, and adaptable to future requirements while providing a clear separation between authentication, test generation, analysis, refactoring, storage, and reporting concerns.
