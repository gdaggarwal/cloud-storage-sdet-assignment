# Cloud Storage Tiering System - Evaluation Criteria

This document outlines the evaluation criteria for the SDET assignment. The maximum possible score is 100 points.

## Code Authenticity Check (Pass/Fail)

Before evaluation, all submissions will be analyzed for AI-generated code patterns. Submissions that show strong indicators of AI generation will be subject to additional scrutiny and may be disqualified if they violate the assignment's AI usage policy.

### Verification Process
1. Automated analysis using our AI detection tool
2. Manual code review for consistency and understanding
3. Verification of problem-solving approach
4. Check for contextual understanding of the requirements

## Part 1: Testing (100% of base score)

### Code Authenticity (20%)
- [ ] Evidence of original thought and problem-solving (5 points)
- [ ] Consistent coding style throughout (5 points)
- [ ] Appropriate level of comments and documentation (5 points)
- [ ] Understanding of contextual requirements (5 points)

### Test Strategy (30%)
- Comprehensive test scenarios covering all requirements
- Identification of edge cases and boundary conditions
- Well-designed test data strategy
- Consideration of performance and security aspects
- Clear documentation of testing approach

### Test Implementation (50%)
- Correctness and completeness of test cases
- Test coverage of all API endpoints and functionality
- Proper error handling and validation
- Code organization and readability
- Use of appropriate test design patterns

### Bug Reporting (20%)
- Accuracy and clarity of bug reports
- Reproduction steps for each issue
- Expected vs actual behavior
- Suggested fixes for critical issues

## 2. Test Implementation (40 points)

### 2.1 Code Quality (10 points)
- [ ] Clean, readable code (3 points)
- [ ] Proper error handling (3 points)
- [ ] Code organization (4 points)

### 2.2 Test Quality (15 points)
- [ ] Meaningful test names (3 points)
- [ ] Independent test cases (4 points)
- [ ] Proper assertions (4 points)
- [ ] Test data management (4 points)

### 2.3 Advanced Testing (15 points)
- [ ] Concurrency testing (5 points)
- [ ] Fault injection (5 points)
- [ ] Data consistency checks (5 points)

## 3. CI/CD Integration (20 points)

### 3.1 Pipeline Configuration (10 points)
- [ ] Automated test execution (5 points)
- [ ] Test result reporting (5 points)

### 3.2 Quality Gates (10 points)
- [ ] Test coverage reporting (5 points)
- [ ] Code quality checks (5 points)

## Automated Test Evaluation

We provide an evaluation script that will automatically run and score the test implementation:

```python
def evaluate_implementation():
    results = {
        'test_strategy': evaluate_test_strategy(),
        'test_implementation': evaluate_test_implementation(),
        'ci_cd': evaluate_ci_cd()
    }
    results['total_score'] = (
        results['test_strategy']['score'] * 0.4 +
        results['test_implementation']['score'] * 0.4 +
        results['ci_cd']['score'] * 0.2
    )
    return results
```

## Scoring Rubric

| Score | Description |
|-------|-------------|
| 90-100 | Exceptional - Exceeds all requirements, demonstrates advanced testing techniques |
| 80-89  | Excellent - Meets all requirements, well-structured tests |
| 70-79  | Good - Meets most requirements, minor issues present |
| 60-69  | Satisfactory - Meets basic requirements, needs improvement |
| Below 60 | Needs Work - Significant improvements needed |

## Review Process

1. Automated test execution
2. Code review for quality and best practices
3. Manual review of test strategy and documentation
4. Performance evaluation under load

## Common Pitfalls to Avoid

- Not testing error conditions
- Ignoring concurrency issues
- Hard-coded test data
- Lack of proper assertions
- Inconsistent test coverage
- Poor error messages in tests
- Not cleaning up test data

## Submission Guidelines

1. Fork the repository
2. Implement your solution
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request with your changes
