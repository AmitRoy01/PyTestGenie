# Preliminary Test Plan for PyTestGenie
## 20 Essential Test Cases for Initial Testing

---

## Module 1: Authentication (3 tests)

### Test Case 1: User Registration
**Test Scenario:** Register a new user successfully.
**Steps:**
1. Send POST request to `/auth/register` with username, email, and password.
2. Verify user created in database.

**Expected Outcome:**
- User is created with hashed password.
- Success response returned.

### Test Case 2: User Login
**Test Scenario:** Login with correct credentials.
**Steps:**
1. Register a user.
2. Login with correct credentials.

**Expected Outcome:**
- Login successful.
- JWT token returned.

### Test Case 3: Token Validation
**Test Scenario:** Access protected routes with token.
**Steps:**
1. Attempt to access protected route without token.
2. Attempt with valid token.

**Expected Outcome:**
- Request without token rejected (401).
- Request with valid token allowed.

---

## Module 2: Test Code Generation (2 tests)

### Test Case 4: Pynguin Test Generation
**Test Scenario:** Generate tests using Pynguin.
**Steps:**
1. Upload a Python file.
2. Select Pynguin method.
3. Execute test generation.

**Expected Outcome:**
- Test file generated successfully.
- Tests are executable.

### Test Case 5: AI/LLM Test Generation
**Test Scenario:** Generate tests using LLM.
**Steps:**
1. Upload a Python file.
2. Select LLM method.
3. Execute test generation.

**Expected Outcome:**
- Test file generated with proper structure.
- Tests are syntactically correct.

---

## Module 3: Test Smell Detection (3 tests)

### Test Case 6: Rule-Based Smell Detection
**Test Scenario:** Detect smells using rules.
**Steps:**
1. Upload test file with known smells.
2. Run rule-based detection.

**Expected Outcome:**
- Smells detected with line numbers.

### Test Case 7: LLM-Based Smell Detection
**Test Scenario:** Detect smells using LLM.
**Steps:**
1. Upload test file.
2. Run LLM-based detection.

**Expected Outcome:**
- Smells detected with explanations.

### Test Case 8: Smell Detection Report
**Test Scenario:** Generate smell detection report.
**Steps:**
1. Run detection on multiple files.
2. Generate report.

**Expected Outcome:**
- Report includes all detected smells.

---

## Module 4: Smell Refactorer (1 test)

### Test Case 9: Refactor Assertion Roulette
**Test Scenario:** Add descriptive messages to assertions.
**Steps:**
1. Select test with Assertion Roulette smell.
2. Initiate refactoring.

**Expected Outcome:**
- Assertions now have descriptive messages.
- Test functionality unchanged.

---

## Module 5: Report Generator (1 test)

### Test Case 10: Generate HTML Report
**Test Scenario:** Create HTML report.
**Steps:**
1. Run smell detection.
2. Generate HTML report.

**Expected Outcome:**
- HTML file created with all results.

---

## Module 6: Dashboard Management (1 test)

### Test Case 11: View Dashboard Overview
**Test Scenario:** User views main dashboard.
**Steps:**
1. Login and navigate to dashboard.

**Expected Outcome:**
- Dashboard displays user statistics.
- Recent activities shown.

---

## Module 7: Artifacts Library (2 tests)

### Test Case 12: List All User Artifacts
**Test Scenario:** View all user artifacts.
**Steps:**
1. Navigate to library.

**Expected Outcome:**
- All artifacts displayed.
- Categorized by type.

### Test Case 13: Delete Artifact
**Test Scenario:** Remove artifact from library.
**Steps:**
1. Select artifact.
2. Delete and confirm.

**Expected Outcome:**
- Artifact removed from library.

---

## Module 8: Tool Configuration (1 test)

### Test Case 14: Configure LLM Settings
**Test Scenario:** Set LLM API keys and parameters.
**Steps:**
1. Enter API key.
2. Set model parameters.
3. Save configuration.

**Expected Outcome:**
- API key stored securely.
- Settings applied to LLM calls.

---

## Module 9: File Upload (2 tests)

### Test Case 15: Upload Single Python File
**Test Scenario:** Upload one .py file.
**Steps:**
1. Select Python file.
2. Upload.

**Expected Outcome:**
- File uploaded successfully.
- Available for processing.

### Test Case 16: File Type Validation
**Test Scenario:** Reject non-Python files.
**Steps:**
1. Attempt to upload .txt file.

**Expected Outcome:**
- Upload rejected with error message.

---

## Module 10: Frontend Components (2 tests)

### Test Case 17: Login Component
**Test Scenario:** Test login functionality.
**Steps:**
1. Enter credentials in Login.jsx.
2. Submit form.

**Expected Outcome:**
- Login request sent.
- User redirected on success.

### Test Case 18: Test Generator Component
**Test Scenario:** Test generation UI.
**Steps:**
1. Upload file in TestGenerator.jsx.
2. Select method.
3. Generate tests.

**Expected Outcome:**
- File uploaded.
- Generation initiated.
- Results displayed.

### Test Case 19: Smell Detector Component
**Test Scenario:** Smell detection UI.
**Steps:**
1. Select files in SmellDetector.jsx.
2. Run detection.

**Expected Outcome:**
- Detection initiated.
- Results displayed.

### Test Case 20: Admin Panel Component
**Test Scenario:** Admin features.
**Steps:**
1. Login as admin.
2. Access AdminPanel.jsx.

**Expected Outcome:**
- Admin features visible.
- User management accessible.

### Test Case 21: Form Validation
**Test Scenario:** Client-side validation.
**Steps:**
1. Submit forms with invalid data.

**Expected Outcome:**
- Validation errors displayed.
- Submission prevented until valid.

---

## Module 11: Admin Module (1 test)

### Test Case 22: Admin Login
**Test Scenario:** Admin authentication.
**Steps:**
1. Login with admin credentials.

**Expected Outcome:**
- Admin authenticated.
- Admin routes accessible.

---

## Module 12: LLM Service Integration (1 test)

### Test Case 23: LLM API Connection
**Test Scenario:** Test API connection.
**Steps:**
1. Configure API key.
2. Send test request.

**Expected Outcome:**
- Connection successful.
- Valid response received.

---

## Test Execution Priority

### Phase 1 - Critical Path (Tests 1-5)
**Priority:** High  
**Focus:** Authentication and Test Generation  
**Duration:** 2-3 days

### Phase 2 - Core Features (Tests 6-13)
**Priority:** High  
**Focus:** Smell Detection, Refactoring, Reports, Artifacts  
**Duration:** 3-4 days

### Phase 3 - Supporting Features (Tests 14-23)
**Priority:** Medium  
**Focus:** Configuration, Upload, Frontend, Admin, LLM  
**Duration:** 3-4 days

---

## Summary

**Total Test Cases:** 23  
**Estimated Testing Duration:** 8-11 days  
**Coverage:** All critical modules with essential functionality

### Module Coverage:
- ✓ Authentication (3)
- ✓ Test Generation (2)
- ✓ Smell Detection (3)
- ✓ Refactoring (1)
- ✓ Reports (1)
- ✓ Dashboard (1)
- ✓ Artifacts (2)
- ✓ Configuration (1)
- ✓ File Upload (2)
- ✓ Frontend (5)
- ✓ Admin (1)
- ✓ LLM Integration (1)

This preliminary test plan focuses on the most critical functionality needed to validate PyTestGenie's core features before expanding to comprehensive testing.
