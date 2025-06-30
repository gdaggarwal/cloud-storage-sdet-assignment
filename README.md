# Cloud Storage Tiering System - SDET Assignment

This repository contains the test automation assignment for SDET candidates at Lucidity. The assignment focuses on testing a Cloud Storage Tiering System that automatically manages data across different storage tiers based on access patterns.

## Problem Statement

See [PROBLEM_STATEMENT.md](docs/PROBLEM_STATEMENT.md) for detailed requirements and tasks.

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gdaggarwal/cloud-storage-sdet-assignment.git
   cd cloud-storage-sdet-assignment
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
cloud-storage-sdet-assignment/
├── docs/                    # Documentation
│   ├── PROBLEM_STATEMENT.md  # Assignment details
│   └── EVALUATION.md        # Evaluation criteria
├── src/                     # Source code
│   └── storage_service.py   # Mock storage service
├── tests/                   # Test files
│   ├── functional/          # Functional tests
│   ├── performance/         # Performance tests
│   └── fault_injection/     # Fault injection tests
├── .github/workflows/       # CI/CD workflows
│   └── tests.yml
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Running Tests

Run all tests:
```bash
pytest tests/
```

Run specific test categories:
```bash
pytest tests/functional/
pytest tests/performance/
pytest tests/fault_injection/
```

## Evaluation

Your submission will be evaluated based on:
1. Test Strategy (40%)
2. Test Implementation (40%)
3. CI/CD Integration (20%)

See [EVALUATION.md](docs/EVALUATION.md) for detailed evaluation criteria.

## Submission

1. Fork this repository
2. Implement your solution
3. Create a pull request with your changes
4. Include any additional documentation or notes in your PR description
