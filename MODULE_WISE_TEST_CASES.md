# Module-Wise Test Cases for PyTestGenie

## Module 1: Authentication Module
**Files:** `backend/routes/auth.py`, `backend/services/auth_service.py`, `backend/middleware/auth.py`

### Test Case 1.1: User Registration with Valid Data
**Test Scenario:** Register a new user successfully.
**Steps:**
1. Send POST request to `/auth/register` with username, email, and password.
2. Verify user created in database.

**Expected Outcome:**
- User is created with hashed password.
- Success response returned.

### Test Case 1.2: User Registration with Duplicate Email
**Test Scenario:** Prevent duplicate email registration.
**Steps:**
1. Register first user with email test@example.com.
2. Attempt to register another user with same email.

**Expected Outcome:**
- Second registration fails with error message.

### Test Case 1.3: User Login with Valid Credentials
**Test Scenario:** Login with correct credentials.
**Steps:**
1. Register a user.
2. Login with correct credentials.

**Expected Outcome:**
- Login successful.
- JWT token returned.

### Test Case 1.4: User Login with Invalid Password
**Test Scenario:** Login attempt with wrong password.
**Steps:**
1. Attempt login with incorrect password.

**Expected Outcome:**
- Login fails with authentication error.

### Test Case 1.5: Token Validation
**Test Scenario:** Access protected routes with token.
**Steps:**
1. Attempt to access protected route without token.
2. Attempt with valid token.

**Expected Outcome:**
- Request without token rejected (401).
- Request with valid token allowed.

### Test Case 1.6: Logout Functionality
**Test Scenario:** User logs out.
**Steps:**
1. Login and obtain token.
2. Logout.
3. Attempt to use same token.

**Expected Outcome:**
- Token invalidated after logout.

---

## Module 2: Test Code Generation Module
**Files:** `backend/modules/test_generator/`, `backend/routes/test_generation.py`

### Test Case 2.1: Pynguin Test Generation
**Test Scenario:** Generate tests using Pynguin.
**Steps:**
1. Upload a Python file.
2. Select Pynguin method.
3. Execute test generation.

**Expected Outcome:**
- Test file generated successfully.
- Tests are executable.

### Test Case 2.2: AI/LLM Test Generation
**Test Scenario:** Generate tests using LLM.
**Steps:**
1. Upload a Python file.
2. Select LLM method.
3. Execute test generation.

**Expected Outcome:**
- Test file generated with proper structure.
- Tests are syntactically correct.

### Test Case 2.3: Combined Generation (Pynguin + LLM)
**Test Scenario:** Generate tests using both methods.
**Steps:**
1. Upload Python code.
2. Select both methods.
3. Generate tests.

**Expected Outcome:**
- Both test versions created.
- User can view and compare both.

### Test Case 2.4: Test Generation Error Handling
**Test Scenario:** Handle invalid Python code.
**Steps:**
1. Upload invalid Python file.
2. Attempt test generation.

**Expected Outcome:**
- Generation fails gracefully with error message.

### Test Case 2.5: Test Generation Progress Tracking
**Test Scenario:** Monitor generation progress.
**Steps:**
1. Upload file and initiate generation.
2. Observe progress indicator.

**Expected Outcome:**
- Progress bar shows status.
- Completion notification displayed.

---

## Module 3: Test Smell Detection Module
**Files:** `backend/modules/smell_detector/`, `backend/routes/smell_detection.py`

### Test Case 3.1: Rule-Based Smell Detection
**Test Scenario:** Detect smells using rules.
**Steps:**
1. Upload test file with known smells.
2. Run rule-based detection.

**Expected Outcome:**
- Smells detected with line numbers.

### Test Case 3.2: LLM-Based Smell Detection
**Test Scenario:** Detect smells using LLM.
**Steps:**
1. Upload test file.
2. Run LLM-based detection.

**Expected Outcome:**
- Smells detected with explanations.

### Test Case 3.3: Detect Assertion Roulette
**Test Scenario:** Identify multiple assertions without messages.
**Steps:**
1. Upload test with multiple assertions.
2. Run detection.

**Expected Outcome:**
- Assertion Roulette smell detected.

### Test Case 3.4: Detect Mystery Guest
**Test Scenario:** Identify external resource dependencies.
**Steps:**
1. Upload test accessing files/database.
2. Run detection.

**Expected Outcome:**
- Mystery Guest smell detected.

### Test Case 3.5: Detect Eager Test
**Test Scenario:** Identify tests testing too many methods.
**Steps:**
1. Upload test with multiple method calls.
2. Run detection.

**Expected Outcome:**
- Eager Test smell detected.

### Test Case 3.6: Smell Detection Report
**Test Scenario:** Generate smell detection report.
**Steps:**
1. Run detection on multiple files.
2. Generate report.

**Expected Outcome:**
- Report includes all detected smells.

---

## Module 4: Smell Refactorer Module
**Files:** Integration with LLM services for refactoring

### Test Case 4.1: Refactor Assertion Roulette
**Test Scenario:** Add descriptive messages to assertions.
**Steps:**
1. Select test with Assertion Roulette smell.
2. Initiate refactoring.

**Expected Outcome:**
- Assertions now have descriptive messages.
- Test functionality unchanged.

### Test Case 4.2: Refactor Eager Test
**Test Scenario:** Split test into multiple focused tests.
**Steps:**
1. Select Eager Test.
2. Initiate refactoring.

**Expected Outcome:**
- Multiple focused tests created.
- All assertions preserved.

### Test Case 4.3: Refactor Mystery Guest
**Test Scenario:** Replace external dependencies with mocks.
**Steps:**
1. Select test with Mystery Guest smell.
2. Initiate refactoring.

**Expected Outcome:**
- External dependencies replaced with mocks.
- Test becomes self-contained.

### Test Case 4.4: Refactoring Preview
**Test Scenario:** Preview changes before applying.
**Steps:**
1. Select test for refactoring.
2. Generate preview.
3. Review and apply.

**Expected Outcome:**
- Diff shown before applying.
- User can confirm or reject.

### Test Case 4.5: Validate Refactored Tests
**Test Scenario:** Ensure refactored tests still pass.
**Steps:**
1. Refactor test code.
2. Run refactored tests.

**Expected Outcome:**
- All tests pass after refactoring.

---

## Module 5: Report Generator Module
**Files:** `backend/modules/smell_detector/report_generator.py`

### Test Case 5.1: Generate HTML Report
**Test Scenario:** Create HTML report.
**Steps:**
1. Run smell detection.
2. Generate HTML report.

**Expected Outcome:**
- HTML file created with all results.

### Test Case 5.2: Generate JSON Report
**Test Scenario:** Export results as JSON.
**Steps:**
1. Run detection.
2. Generate JSON report.

**Expected Outcome:**
- Valid JSON file created.

### Test Case 5.3: Report with Code Snippets
**Test Scenario:** Include code in report.
**Steps:**
1. Generate report with snippets enabled.

**Expected Outcome:**
- Code snippets included with syntax highlighting.

### Test Case 5.4: Comparative Report
**Test Scenario:** Compare before/after refactoring.
**Steps:**
1. Run detection on original and refactored code.
2. Generate comparative report.

**Expected Outcome:**
- Side-by-side comparison shown.
- Improvements highlighted.

---

## Module 6: Dashboard Management Module
**Files:** `frontend/src/components/`, Dashboard APIs

### Test Case 6.1: View Dashboard Overview
**Test Scenario:** User views main dashboard.
**Steps:**
1. Login and navigate to dashboard.

**Expected Outcome:**
- Dashboard displays user statistics.
- Recent activities shown.

### Test Case 6.2: View Test Generation Statistics
**Test Scenario:** Display test generation metrics.
**Steps:**
1. Access statistics section.

**Expected Outcome:**
- Total tests generated shown.
- Success rate displayed.

### Test Case 6.3: View Smell Detection Statistics
**Test Scenario:** Display smell detection metrics.
**Steps:**
1. Access smell statistics.

**Expected Outcome:**
- Total smells detected shown.
- Breakdown by type displayed.

### Test Case 6.4: View Recent Activities
**Test Scenario:** Display user's recent actions.
**Steps:**
1. Check recent activities widget.

**Expected Outcome:**
- Last 10 activities listed with timestamps.

### Test Case 6.5: Quick Actions
**Test Scenario:** Access quick action buttons.
**Steps:**
1. Use quick action buttons from dashboard.

**Expected Outcome:**
- Quick access to generation/detection features.

---

## Module 7: Artifacts Library Management Module
**Files:** Backend artifact management logic

### Test Case 7.1: List All User Artifacts
**Test Scenario:** View all user artifacts.
**Steps:**
1. Navigate to library.

**Expected Outcome:**
- All artifacts displayed.
- Categorized by type.

### Test Case 7.2: Retrieve Specific Artifact
**Test Scenario:** Open/download artifact.
**Steps:**
1. Select artifact.
2. Open or download.

**Expected Outcome:**
- Artifact content displayed/downloaded.

### Test Case 7.3: Delete Artifact
**Test Scenario:** Remove artifact from library.
**Steps:**
1. Select artifact.
2. Delete and confirm.

**Expected Outcome:**
- Artifact removed from library.

### Test Case 7.4: Search Artifacts
**Test Scenario:** Find specific artifact.
**Steps:**
1. Enter search term.
2. View results.

**Expected Outcome:**
- Relevant artifacts returned.

### Test Case 7.5: Artifact Access Control
**Test Scenario:** Users can only access their own artifacts.
**Steps:**
1. Login as User A.
2. Verify only User A's artifacts visible.

**Expected Outcome:**
- User sees only their artifacts.

---

## Module 8: Tool Configuration Module
**Files:** `backend/config/settings.py`, Configuration management

### Test Case 8.1: Configure Pynguin Settings
**Test Scenario:** Set Pynguin generation parameters.
**Steps:**
1. Access configuration.
2. Set timeout, algorithm.
3. Save settings.

**Expected Outcome:**
- Settings saved.
- Applied to next generation.

### Test Case 8.2: Configure LLM Settings
**Test Scenario:** Set LLM API keys and parameters.
**Steps:**
1. Enter API key.
2. Set model parameters.
3. Save configuration.

**Expected Outcome:**
- API key stored securely.
- Settings applied to LLM calls.

### Test Case 8.3: Configure Smell Detection Rules
**Test Scenario:** Enable/disable specific smell types.
**Steps:**
1. Access smell detection config.
2. Toggle smell types.
3. Save changes.

**Expected Outcome:**
- Only enabled smells detected.

### Test Case 8.4: Configure Report Settings
**Test Scenario:** Set default report format and options.
**Steps:**
1. Select default format (HTML/JSON/PDF).
2. Configure report sections.
3. Save preferences.

**Expected Outcome:**
- Preferences saved.
- Applied to future reports.

### Test Case 8.5: View Configuration History
**Test Scenario:** Track configuration changes.
**Steps:**
1. Access configuration history.

**Expected Outcome:**
- Previous configurations listed with timestamps.

---

## Module 9: File Upload Module
**Files:** `backend/routes/test_generation.py`, Upload handling

### Test Case 9.1: Upload Single Python File
**Test Scenario:** Upload one .py file.
**Steps:**
1. Select Python file.
2. Upload.

**Expected Outcome:**
- File uploaded successfully.
- Available for processing.

### Test Case 9.2: Upload Multiple Files
**Test Scenario:** Upload multiple files at once.
**Steps:**
1. Select multiple .py files.
2. Upload.

**Expected Outcome:**
- All files uploaded.

### Test Case 9.3: File Type Validation
**Test Scenario:** Reject non-Python files.
**Steps:**
1. Attempt to upload .txt file.

**Expected Outcome:**
- Upload rejected with error message.

### Test Case 9.4: Upload via Code Paste
**Test Scenario:** Paste code directly.
**Steps:**
1. Paste Python code in text area.
2. Save.

**Expected Outcome:**
- Code saved as file.

### Test Case 9.5: File Size Limit
**Test Scenario:** Enforce upload size limit.
**Steps:**
1. Attempt to upload very large file.

**Expected Outcome:**
- Upload rejected if exceeds limit.

---

## Module 10: Frontend Components Module
**Files:** `frontend/src/components/`

### Test Case 10.1: Login Component
**Test Scenario:** Test login functionality.
**Steps:**
1. Enter credentials in Login.jsx.
2. Submit form.

**Expected Outcome:**
- Login request sent.
- User redirected on success.

### Test Case 10.2: Test Generator Component
**Test Scenario:** Test generation UI.
**Steps:**
1. Upload file in TestGenerator.jsx.
2. Select method.
3. Generate tests.

**Expected Outcome:**
- File uploaded.
- Generation initiated.
- Results displayed.

### Test Case 10.3: Smell Detector Component
**Test Scenario:** Smell detection UI.
**Steps:**
1. Select files in SmellDetector.jsx.
2. Run detection.

**Expected Outcome:**
- Detection initiated.
- Results displayed.

### Test Case 10.4: Admin Panel Component
**Test Scenario:** Admin features.
**Steps:**
1. Login as admin.
2. Access AdminPanel.jsx.

**Expected Outcome:**
- Admin features visible.
- User management accessible.

### Test Case 10.5: Responsive Design
**Test Scenario:** Test on different screen sizes.
**Steps:**
1. View on desktop, tablet, mobile.

**Expected Outcome:**
- Layout adapts to screen size.

### Test Case 10.6: Form Validation
**Test Scenario:** Client-side validation.
**Steps:**
1. Submit forms with invalid data.

**Expected Outcome:**
- Validation errors displayed.
- Submission prevented until valid.

---

## Module 11: Admin Module
**Files:** `backend/routes/admin.py`

### Test Case 11.1: Admin Login
**Test Scenario:** Admin authentication.
**Steps:**
1. Login with admin credentials.

**Expected Outcome:**
- Admin authenticated.
- Admin routes accessible.

### Test Case 11.2: View All Users
**Test Scenario:** List registered users.
**Steps:**
1. Access user list.

**Expected Outcome:**
- All users displayed.

### Test Case 11.3: Delete User Account
**Test Scenario:** Admin deletes user.
**Steps:**
1. Select user.
2. Delete and confirm.

**Expected Outcome:**
- User account deleted.

### Test Case 11.4: View System Statistics
**Test Scenario:** View usage metrics.
**Steps:**
1. Access statistics dashboard.

**Expected Outcome:**
- Total users, tests, smells displayed.

### Test Case 11.5: Non-Admin Access Prevention
**Test Scenario:** Regular user cannot access admin.
**Steps:**
1. Login as regular user.
2. Attempt admin access.

**Expected Outcome:**
- Access denied (403).

---

## Module 12: LLM Service Integration Module
**Files:** `backend/services/gemini_service.py`, `explanation_fallback.py`

### Test Case 12.1: LLM API Connection
**Test Scenario:** Test API connection.
**Steps:**
1. Configure API key.
2. Send test request.

**Expected Outcome:**
- Connection successful.
- Valid response received.

### Test Case 12.2: Test Generation via LLM
**Test Scenario:** Generate tests using LLM.
**Steps:**
1. Provide source code.
2. Request test generation.

**Expected Outcome:**
- Tests generated.
- Syntactically correct.

### Test Case 12.3: Explanation Generation
**Test Scenario:** Generate code explanation.
**Steps:**
1. Provide code snippet.
2. Request explanation.

**Expected Outcome:**
- Explanation generated.
- Clear and relevant.

### Test Case 12.4: Fallback Mechanism
**Test Scenario:** Handle API failure.
**Steps:**
1. Simulate API failure.
2. Request service.

**Expected Outcome:**
- Fallback activated.
- User receives response.

### Test Case 12.5: Response Sanitization
**Test Scenario:** Clean LLM responses.
**Steps:**
1. Request code generation.
2. Verify response cleaned.

**Expected Outcome:**
- Code extracted from markdown.
- Safe output provided.

---

## Summary

This test suite covers **12 essential modules** with **streamlined, practical test cases**:

1. **Authentication** - User registration, login, token management (6 tests)
2. **Test Code Generation** - Pynguin, LLM, combined methods (5 tests)
3. **Test Smell Detection** - Rule-based, LLM-based detection (6 tests)
4. **Smell Refactorer** - Automated refactoring with LLM (5 tests)
5. **Report Generator** - HTML, JSON, comparative reports (4 tests)
6. **Dashboard Management** - User dashboard and statistics (5 tests)
7. **Artifacts Library** - File management and access control (5 tests)
8. **Tool Configuration** - Settings for all modules (5 tests)
9. **File Upload** - Upload validation and handling (5 tests)
10. **Frontend Components** - React UI components (6 tests)
11. **Admin Module** - Administrative functions (5 tests)
12. **LLM Service Integration** - AI service integration (5 tests)

**Total:** ~62 focused, essential test cases covering all critical functionality without unnecessary complexity.
