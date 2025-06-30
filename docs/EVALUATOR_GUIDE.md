# Evaluator Guide: Cloud Storage Tiering System - SDET Assignment

This guide provides instructions for evaluating candidate submissions for the SDET position at Lucidity.

## Evaluation Criteria Overview

Candidates will be evaluated on three main areas:

1. **Test Strategy (40 points)**
   - Test coverage and scenarios
   - Edge case consideration
   - Performance testing approach
   - Reliability testing

2. **Test Implementation (40 points)**
   - Code quality and organization
   - Test quality and assertions
   - Advanced testing techniques

3. **CI/CD Integration (20 points)**
   - Pipeline configuration
   - Quality gates and reporting

## Step-by-Step Evaluation Process

### 1. Initial Setup

1. Clone the candidate's repository:
   ```bash
   git clone <candidate-repo-url>
   cd cloud-storage-sdet-assignment
   ```

2. Set up the environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 2. Automated Test Execution

Run the test suites using the provided runner:

```bash
# Run all tests
python run_tests.py all --coverage

# Run specific test types
python run_tests.py functional
python run_tests.py performance
python run_tests.py fault
```

### 3. Manual Code Review

Examine the following aspects of the candidate's code:

#### Test Strategy
- [ ] Are all API endpoints covered by tests?
- [ ] Are edge cases considered (e.g., large files, concurrent access)?
- [ ] Is there a clear performance testing strategy?
- [ ] Are reliability aspects tested (e.g., error handling, fault tolerance)?

#### Test Implementation
- [ ] Is the code well-organized and readable?
- [ ] Are test cases independent and idempotent?
- [ ] Are assertions meaningful and specific?
- [ ] Is test data managed effectively?
- [ ] Are there tests for concurrent access scenarios?
- [ ] Are fault injection tests present?

#### CI/CD Integration
- [ ] Is there a working CI/CD pipeline configuration?
- [ ] Are test results properly reported?
- [ ] Is there test coverage reporting?
- [ ] Are there quality gates in place?

### 4. Performance Evaluation

Run the performance tests and evaluate:

```bash
python run_tests.py performance -v
```

Check for:
- Reasonable test execution time
- Proper resource usage
- Appropriate assertions for performance criteria

### 5. Fault Injection Evaluation

Run the fault injection tests:

```bash
python run_tests.py fault -v
```

Verify that the tests properly simulate and handle:
- Network failures
- Storage failures
- Concurrent modifications
- Corrupted data

## Scoring Rubric

Use the following rubric to assign scores:

### Test Strategy (40 points)
- **15 points**: Test coverage and scenarios
- **10 points**: Edge case consideration
- **10 points**: Performance testing approach
- **5 points**: Reliability testing

### Test Implementation (40 points)
- **10 points**: Code quality and organization
- **15 points**: Test quality and assertions
- **15 points**: Advanced testing techniques

### CI/CD Integration (20 points)
- **10 points**: Pipeline configuration
- **10 points**: Quality gates and reporting

## Common Issues to Watch For

1. **Insufficient Test Coverage**
   - Missing tests for error conditions
   - Lack of boundary value testing
   - Incomplete API endpoint coverage

2. **Brittle Tests**
   - Tests that depend on specific timing
   - Non-deterministic test cases
   - Tests that depend on external services

3. **Poor Error Handling**
   - Generic assertions
   - Lack of proper error messages
   - No cleanup of test data

4. **Performance Issues**
   - Tests that are too slow
   - Excessive resource usage
   - No performance assertions

5. **Lack of Documentation**
   - Missing or unclear test descriptions
   - No setup instructions
   - Lack of comments explaining complex test logic

## Sample Evaluation Notes

### Strong Candidate
- Comprehensive test coverage of all requirements
- Well-organized, maintainable test code
- Thoughtful consideration of edge cases
- Effective use of advanced testing techniques
- Clean CI/CD integration

### Average Candidate
- Good coverage of main functionality
- Some edge cases may be missing
- Basic test organization
- Functional but basic CI/CD setup

### Needs Improvement
- Incomplete test coverage
- Poorly organized or hard-to-maintain tests
- Missing important test cases
- No or broken CI/CD integration

## Final Assessment

After completing the evaluation:

1. Calculate the total score (out of 100)
2. Provide detailed feedback on strengths and areas for improvement
3. Make a hiring recommendation based on the evaluation criteria

## Example Feedback

```
Strengths:
- Excellent test coverage of all API endpoints
- Well-structured and maintainable test code
- Good consideration of edge cases
- Effective use of performance testing

Areas for Improvement:
- Could add more fault injection tests
- Some test cases could be more specific in their assertions
- Consider adding more detailed documentation

Score: 85/100
Recommendation: Strong candidate, recommend moving forward
```
