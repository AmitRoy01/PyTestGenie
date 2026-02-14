# Database Modeling - PyTestGenie

## Overview

Database modeling is a technique used to visually represent the structure of a database and how data is organized within a system. It involves creating entity-relationship diagrams (ERDs) that show tables (entities), their attributes (columns), and the relationships between them.

For PyTestGenie, the database supports user authentication, user library management, test generation tracking, smell detection results, refactoring history, and report generation. The database is designed to maintain relationships between users, their projects, source files, generated tests, detected smells, and evaluation reports.

---

## Entity-Relationship Diagram (ERD)

```
┌─────────────────┐
│     User        │
│─────────────────│
│ id (PK)         │───┐
│ username        │   │
│ email           │   │
│ password_hash   │   │
│ role            │   │
│ status          │   │
│ created_at      │   │
│ updated_at      │   │
└─────────────────┘   │
                      │
                      │ 1:N
                      │
                      ▼
┌─────────────────────────────┐         ┌─────────────────────────┐
│      Project                │         │    UserSettings         │
│─────────────────────────────│         │─────────────────────────│
│ id (PK)                     │◄────────│ id (PK)                 │
│ user_id (FK)                │   1:1   │ user_id (FK)            │
│ project_name                │         │ default_algorithm       │
│ description                 │         │ default_llm_model       │
│ created_at                  │         │ display_name            │
│ updated_at                  │         │ notifications_enabled   │
└─────────────────────────────┘         │ theme                   │
           │                            │ created_at              │
           │ 1:N                        │ updated_at              │
           │                            └─────────────────────────┘
           ▼
┌─────────────────────────────┐
│      SourceFile             │
│─────────────────────────────│
│ id (PK)                     │
│ project_id (FK)             │
│ file_name                   │
│ file_path                   │
│ file_content                │
│ file_size                   │
│ upload_type                 │──────► ('upload', 'paste')
│ created_at                  │
│ updated_at                  │
└─────────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────────┐
│      GeneratedTest          │
│─────────────────────────────│
│ id (PK)                     │
│ source_file_id (FK)         │
│ test_file_name              │
│ test_content                │
│ generation_method           │──────► ('pynguin', 'llm')
│ llm_model_used              │
│ algorithm_used              │
│ coverage_percentage         │
│ execution_time              │
│ status                      │──────► ('success', 'failed', 'partial')
│ created_at                  │
└─────────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────────┐
│    SmellDetectionReport     │
│─────────────────────────────│
│ id (PK)                     │
│ generated_test_id (FK)      │
│ detection_method            │──────► ('rule_based', 'llm', 'multi_agent')
│ llm_model_used              │
│ total_smells_detected       │
│ execution_time              │
│ status                      │
│ created_at                  │
└─────────────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────────┐
│      DetectedSmell          │
│─────────────────────────────│
│ id (PK)                     │
│ report_id (FK)              │
│ smell_type                  │──────► (assertion_roulette, eager_test, etc.)
│ severity                    │──────► ('critical', 'high', 'medium', 'low')
│ line_number                 │
│ code_snippet                │
│ description                 │
│ confidence_score            │
│ created_at                  │
└─────────────────────────────┘
           │
           │ 1:1
           │
           ▼
┌─────────────────────────────┐
│     RefactoredCode          │
│─────────────────────────────│
│ id (PK)                     │
│ detected_smell_id (FK)      │
│ original_code               │
│ refactored_code             │
│ refactoring_method          │──────► ('llm', 'multi_agent')
│ llm_model_used              │
│ agents_used                 │
│ refactoring_strategy        │
│ status                      │──────► ('success', 'failed', 'pending')
│ validation_passed           │
│ execution_time              │
│ created_at                  │
└─────────────────────────────┘
           │
           │ N:1
           │
           ▼
┌─────────────────────────────┐
│    EvaluationReport         │
│─────────────────────────────│
│ id (PK)                     │
│ project_id (FK)             │
│ report_name                 │
│ report_type                 │──────► ('detection', 'refactoring', 'comparative')
│ total_tests_generated       │
│ total_smells_detected       │
│ total_refactorings          │
│ detection_accuracy          │
│ refactoring_success_rate    │
│ coverage_improvement        │
│ report_content_json         │
│ report_file_path            │
│ created_at                  │
└─────────────────────────────┘
```

---

## Database Schema

### 1. User
Stores user account information and authentication details.

| Attribute       | Type           | Constraints                    | Description                              |
|----------------|----------------|--------------------------------|------------------------------------------|
| id             | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique user identifier                   |
| username       | VARCHAR(50)    | UNIQUE, NOT NULL               | User's username                          |
| email          | VARCHAR(100)   | UNIQUE, NOT NULL               | User's email address                     |
| password_hash  | VARCHAR(255)   | NOT NULL                       | Hashed password                          |
| role           | ENUM           | ('admin', 'user'), DEFAULT 'user' | User role for access control          |
| status         | ENUM           | ('pending', 'active', 'suspended'), DEFAULT 'pending' | Account status |
| created_at     | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Account creation timestamp               |
| updated_at     | DATETIME       | ON UPDATE CURRENT_TIMESTAMP    | Last update timestamp                    |

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE INDEX (username)
- UNIQUE INDEX (email)
- INDEX (status)

---

### 2. UserSettings
Stores user preferences and default configurations.

| Attribute               | Type           | Constraints                    | Description                              |
|------------------------|----------------|--------------------------------|------------------------------------------|
| id                     | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique settings identifier               |
| user_id                | INT            | FOREIGN KEY → User(id), UNIQUE | Reference to user                        |
| display_name           | VARCHAR(100)   | NULL                           | Display name for dashboard               |
| default_algorithm      | VARCHAR(50)    | DEFAULT 'WHOLE_SUITE'          | Default Pynguin algorithm                |
| default_llm_model      | VARCHAR(50)    | DEFAULT 'gemini'               | Default LLM model                        |
| notifications_enabled  | BOOLEAN        | DEFAULT TRUE                   | Email notification preference            |
| theme                  | VARCHAR(20)    | DEFAULT 'light'                | UI theme preference                      |
| created_at             | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Settings creation timestamp              |
| updated_at             | DATETIME       | ON UPDATE CURRENT_TIMESTAMP    | Last update timestamp                    |

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id)
- FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE

---

### 3. Project
Organizes user files into logical projects/folders.

| Attribute      | Type           | Constraints                    | Description                              |
|---------------|----------------|--------------------------------|------------------------------------------|
| id            | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique project identifier                |
| user_id       | INT            | FOREIGN KEY → User(id)         | Owner of the project                     |
| project_name  | VARCHAR(100)   | NOT NULL                       | Name of the project                      |
| description   | TEXT           | NULL                           | Project description                      |
| created_at    | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Project creation timestamp               |
| updated_at    | DATETIME       | ON UPDATE CURRENT_TIMESTAMP    | Last update timestamp                    |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (user_id)
- FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE

---

### 4. SourceFile
Stores uploaded or pasted Python source code files.

| Attribute      | Type           | Constraints                    | Description                              |
|---------------|----------------|--------------------------------|------------------------------------------|
| id            | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique file identifier                   |
| project_id    | INT            | FOREIGN KEY → Project(id)      | Project this file belongs to             |
| file_name     | VARCHAR(255)   | NOT NULL                       | Name of the source file                  |
| file_path     | VARCHAR(500)   | NULL                           | Path to stored file                      |
| file_content  | TEXT           | NOT NULL                       | Content of the source code               |
| file_size     | INT            | NULL                           | File size in bytes                       |
| upload_type   | ENUM           | ('upload', 'paste'), NOT NULL  | How the file was added                   |
| created_at    | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | File upload timestamp                    |
| updated_at    | DATETIME       | ON UPDATE CURRENT_TIMESTAMP    | Last update timestamp                    |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (project_id)
- FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE

---

### 5. GeneratedTest
Stores generated unit test files and metadata.

| Attribute           | Type           | Constraints                    | Description                              |
|--------------------|----------------|--------------------------------|------------------------------------------|
| id                 | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique test identifier                   |
| source_file_id     | INT            | FOREIGN KEY → SourceFile(id)   | Source file this test was generated from |
| test_file_name     | VARCHAR(255)   | NOT NULL                       | Name of the test file                    |
| test_content       | TEXT           | NOT NULL                       | Content of the generated test            |
| generation_method  | ENUM           | ('pynguin', 'llm'), NOT NULL   | Method used to generate test             |
| llm_model_used     | VARCHAR(50)    | NULL                           | LLM model name if used                   |
| algorithm_used     | VARCHAR(50)    | NULL                           | Pynguin algorithm if used                |
| coverage_percentage| DECIMAL(5,2)   | NULL                           | Code coverage achieved                   |
| execution_time     | DECIMAL(10,2)  | NULL                           | Time taken to generate (seconds)         |
| status             | ENUM           | ('success', 'failed', 'partial'), DEFAULT 'success' | Generation status |
| created_at         | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Test generation timestamp                |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (source_file_id)
- INDEX (generation_method)
- FOREIGN KEY (source_file_id) REFERENCES SourceFile(id) ON DELETE CASCADE

---

### 6. SmellDetectionReport
Stores test smell detection analysis reports.

| Attribute              | Type           | Constraints                    | Description                              |
|-----------------------|----------------|--------------------------------|------------------------------------------|
| id                    | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique report identifier                 |
| generated_test_id     | INT            | FOREIGN KEY → GeneratedTest(id)| Test file analyzed                       |
| detection_method      | ENUM           | ('rule_based', 'llm', 'multi_agent'), NOT NULL | Detection approach |
| llm_model_used        | VARCHAR(50)    | NULL                           | LLM model if used                        |
| total_smells_detected | INT            | DEFAULT 0                      | Number of smells found                   |
| execution_time        | DECIMAL(10,2)  | NULL                           | Time taken for detection (seconds)       |
| status                | ENUM           | ('completed', 'failed', 'in_progress'), DEFAULT 'completed' | Report status |
| created_at            | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Detection timestamp                      |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (generated_test_id)
- INDEX (detection_method)
- FOREIGN KEY (generated_test_id) REFERENCES GeneratedTest(id) ON DELETE CASCADE

---

### 7. DetectedSmell
Stores individual detected test smells with details.

| Attribute         | Type           | Constraints                    | Description                              |
|------------------|----------------|--------------------------------|------------------------------------------|
| id               | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique smell identifier                  |
| report_id        | INT            | FOREIGN KEY → SmellDetectionReport(id) | Parent report                   |
| smell_type       | VARCHAR(100)   | NOT NULL                       | Type of smell (e.g., assertion_roulette) |
| severity         | ENUM           | ('critical', 'high', 'medium', 'low'), DEFAULT 'medium' | Severity level |
| line_number      | INT            | NULL                           | Line where smell occurs                  |
| code_snippet     | TEXT           | NULL                           | Code fragment with smell                 |
| description      | TEXT           | NULL                           | Explanation of the smell                 |
| confidence_score | DECIMAL(3,2)   | NULL                           | Detection confidence (0.00-1.00)         |
| created_at       | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Detection timestamp                      |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (report_id)
- INDEX (smell_type)
- INDEX (severity)
- FOREIGN KEY (report_id) REFERENCES SmellDetectionReport(id) ON DELETE CASCADE

---

### 8. RefactoredCode
Stores refactored test code and refactoring metadata.

| Attribute            | Type           | Constraints                    | Description                              |
|---------------------|----------------|--------------------------------|------------------------------------------|
| id                  | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique refactoring identifier            |
| detected_smell_id   | INT            | FOREIGN KEY → DetectedSmell(id)| Smell being refactored                   |
| original_code       | TEXT           | NOT NULL                       | Original code with smell                 |
| refactored_code     | TEXT           | NOT NULL                       | Refactored clean code                    |
| refactoring_method  | ENUM           | ('llm', 'multi_agent'), NOT NULL | Refactoring approach                  |
| llm_model_used      | VARCHAR(50)    | NULL                           | LLM model used                           |
| agents_used         | VARCHAR(200)   | NULL                           | Agent roles in multi-agent workflow      |
| refactoring_strategy| VARCHAR(100)   | NULL                           | Strategy applied (e.g., extract_method)  |
| status              | ENUM           | ('success', 'failed', 'pending'), DEFAULT 'pending' | Refactoring status |
| validation_passed   | BOOLEAN        | DEFAULT FALSE                  | Whether validation tests passed          |
| execution_time      | DECIMAL(10,2)  | NULL                           | Time taken (seconds)                     |
| created_at          | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Refactoring timestamp                    |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (detected_smell_id)
- INDEX (status)
- FOREIGN KEY (detected_smell_id) REFERENCES DetectedSmell(id) ON DELETE CASCADE

---

### 9. EvaluationReport
Stores comprehensive evaluation and comparison reports.

| Attribute                | Type           | Constraints                    | Description                              |
|-------------------------|----------------|--------------------------------|------------------------------------------|
| id                      | INT            | PRIMARY KEY, AUTO_INCREMENT    | Unique report identifier                 |
| project_id              | INT            | FOREIGN KEY → Project(id)      | Project this report belongs to           |
| report_name             | VARCHAR(200)   | NOT NULL                       | Name of the report                       |
| report_type             | ENUM           | ('detection', 'refactoring', 'comparative', 'full_pipeline') | Report category |
| total_tests_generated   | INT            | DEFAULT 0                      | Total tests in this evaluation           |
| total_smells_detected   | INT            | DEFAULT 0                      | Total smells found                       |
| total_refactorings      | INT            | DEFAULT 0                      | Total refactorings performed             |
| detection_accuracy      | DECIMAL(5,2)   | NULL                           | Detection accuracy percentage            |
| refactoring_success_rate| DECIMAL(5,2)   | NULL                           | Refactoring success rate                 |
| coverage_improvement    | DECIMAL(5,2)   | NULL                           | Coverage improvement percentage          |
| report_content_json     | JSON           | NULL                           | Detailed metrics in JSON format          |
| report_file_path        | VARCHAR(500)   | NULL                           | Path to exported report file             |
| created_at              | DATETIME       | DEFAULT CURRENT_TIMESTAMP      | Report generation timestamp              |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (project_id)
- INDEX (report_type)
- FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE

---

## Relationships Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| User ↔ Project | 1:N | One user can have multiple projects |
| User ↔ UserSettings | 1:1 | Each user has one settings record |
| Project ↔ SourceFile | 1:N | One project contains multiple files |
| SourceFile ↔ GeneratedTest | 1:N | One source file can have multiple tests |
| GeneratedTest ↔ SmellDetectionReport | 1:N | One test can have multiple detection reports |
| SmellDetectionReport ↔ DetectedSmell | 1:N | One report contains multiple detected smells |
| DetectedSmell ↔ RefactoredCode | 1:1 | Each smell has one refactoring record |
| Project ↔ EvaluationReport | 1:N | One project can have multiple evaluation reports |

---

## Key Design Decisions

### 1. Cascade Deletion
- When a user is deleted, all associated projects, files, tests, and reports are automatically deleted
- This maintains referential integrity and prevents orphaned records

### 2. Status Tracking
- All major entities include status fields to track workflow progress
- Enables querying for incomplete or failed operations

### 3. Temporal Data
- All entities include `created_at` and most include `updated_at` timestamps
- Supports auditing and tracking user activity over time

### 4. Flexible Content Storage
- Large content (source code, test code) stored as TEXT
- JSON fields for complex structured data (evaluation reports)
- File paths stored separately for optional file system storage

### 5. Method Tracking
- Generation method, detection method, and refactoring method are tracked
- Enables comparative analysis between different approaches

### 6. Metadata Richness
- LLM models, algorithms, execution times, and confidence scores tracked
- Supports detailed reporting and analysis

---

## Sample Queries

### Get all projects for a user with file counts
```sql
SELECT p.id, p.project_name, COUNT(sf.id) as file_count
FROM Project p
LEFT JOIN SourceFile sf ON p.id = sf.project_id
WHERE p.user_id = ?
GROUP BY p.id, p.project_name
ORDER BY p.updated_at DESC;
```

### Get test generation statistics for a project
```sql
SELECT 
    generation_method,
    COUNT(*) as total_tests,
    AVG(coverage_percentage) as avg_coverage,
    AVG(execution_time) as avg_time
FROM GeneratedTest gt
JOIN SourceFile sf ON gt.source_file_id = sf.id
WHERE sf.project_id = ?
GROUP BY generation_method;
```

### Get most common test smells detected
```sql
SELECT 
    smell_type,
    COUNT(*) as occurrence_count,
    AVG(confidence_score) as avg_confidence
FROM DetectedSmell
GROUP BY smell_type
ORDER BY occurrence_count DESC
LIMIT 10;
```

### Get refactoring success rate by method
```sql
SELECT 
    refactoring_method,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
    ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
FROM RefactoredCode
GROUP BY refactoring_method;
```

---

## Database Technology Stack

**Primary Database:** PostgreSQL 14+  
**Reasons:**
- Robust JSON support for complex report data
- Strong ACID compliance for data integrity
- Excellent performance for analytical queries
- Native support for arrays and complex types

**Alternative:** SQLite (for development/testing)  
- Lightweight and embedded
- No separate server required
- Easy setup for local development

**ORM:** SQLAlchemy  
- Python-native ORM
- Database-agnostic (supports PostgreSQL, SQLite, MySQL)
- Migration support via Alembic

---

## Database Optimization Strategies

1. **Indexing**: Strategic indexes on foreign keys and frequently queried fields
2. **Partitioning**: Consider partitioning large tables (DetectedSmell, RefactoredCode) by date
3. **Archiving**: Move old reports to archive tables after 1 year
4. **Caching**: Cache user settings and frequently accessed project metadata
5. **Connection Pooling**: Use connection pooling (via SQLAlchemy) for better performance
