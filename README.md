# Cloud Storage Tiering# Cloud Storage SDET Assignment

Welcome to the Cloud Storage Tiering System assignment! This assignment is designed to evaluate your skills in test automation and software development.

## IMPORTANT: AI/LLM Usage Policy

**The use of AI/LLM tools (including but not limited to ChatGPT, GitHub Copilot, etc.) is strictly prohibited for this assignment.**

We employ advanced detection tools to identify AI-generated solutions. Any submission found to be generated or significantly assisted by AI/LLM tools will be automatically disqualified. This assignment is designed to evaluate your personal skills and understanding, and we want to ensure a fair evaluation for all candidates.

### What we're looking for:
- Your unique problem-solving approach
- Your understanding of testing principles
- Your ability to write clean, maintainable code
- Your attention to edge cases and error handling

### What we're not looking for:
- Perfectly polished AI-generated solutions
- Code that doesn't reflect your personal understanding
- Solutions that don't address the specific requirements

## Assignment Overview

This is a two-part assignment:
1. **Required**: Test the provided Cloud Storage Tiering System implementation
2. **Bonus**: Implement improvements and new features

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
