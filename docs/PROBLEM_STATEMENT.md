# Cloud Storage Tiering System - SDET Assignment

## Overview
Design and implement test automation for a Cloud Storage Tiering System that automatically moves data between different storage tiers based on access patterns and policies.

## Problem Statement

### System Architecture
You'll be testing a Cloud Storage Tiering System with the following components:

1. **Storage Tiers**:
   - **Hot Tier**: High-performance, low-latency storage (SSD)
   - **Warm Tier**: Standard performance storage (HDD)
   - **Cold Tier**: Low-cost, high-latency storage (Object Storage)

2. **Tiering Policies**:
   - Files not accessed for 30 days move from Hot → Warm
   - Files not accessed for 90 days move from Warm → Cold
   - Frequently accessed files move up tiers (Cold → Warm → Hot)
   - Minimum file size for tiering: 1MB
   - Maximum file size: 10GB

### API Endpoints

#### File Operations
- `POST /files` - Upload a new file
  - Request: Multipart form with file data
  - Response: `{ "fileId": "uuid", "tier": "HOT" }`

- `GET /files/{fileId}` - Download a file
  - Response: File content with appropriate headers

- `GET /files/{fileId}/metadata` - Get file metadata
  - Response: `{ "fileId": "uuid", "size": 1024, "lastAccessed": "2023-01-01T00:00:00Z", "tier": "HOT" }`

- `DELETE /files/{fileId}` - Delete a file

#### Admin Operations
- `POST /admin/tiering/run` - Manually trigger tiering process
  - Response: `{ "status": "success", "filesMoved": 5 }`

- `GET /admin/stats` - Get system statistics
  - Response: `{ "totalFiles": 100, "hotTier": { "count": 30, "size": "300MB" }, ... }`

### Your Tasks

1. **Test Strategy (40%)**
   - Design a comprehensive test strategy document
   - Identify test scenarios including edge cases
   - Define test data requirements
   - Consider performance and reliability aspects

2. **Test Automation (40%)**
   - Implement automated tests for all API endpoints
   - Include tests for data consistency and integrity
   - Implement performance tests for tiering operations
   - Add fault injection tests for system reliability
   - Test concurrent access scenarios

3. **CI/CD Integration (20%)**
   - Set up GitHub Actions workflow for test execution
   - Include test reporting
   - Add appropriate test coverage reporting

### Deliverables
1. Source code for all test automation
2. Test documentation including test cases and results
3. CI/CD pipeline configuration
4. A README with setup and execution instructions

## Evaluation Criteria

Your submission will be evaluated based on:

1. **Test Strategy (40 points)**
   - Completeness of test scenarios
   - Identification of edge cases
   - Performance testing approach
   - Reliability considerations

2. **Test Implementation (40 points)**
   - Code quality and organization
   - Test coverage
   - Quality of assertions
   - Error handling
   - Concurrency testing

3. **CI/CD Integration (20 points)**
   - Pipeline configuration
   - Test reporting
   - Automation level

## Getting Started

1. Fork this repository
2. Set up your development environment
3. Implement your solution
4. Document your approach and findings
5. Submit a pull request with your changes

## Time Allocation

We expect this assignment to take approximately 4-6 hours to complete. Focus on quality over quantity - it's better to have fewer, well-thought-out tests than many superficial ones.

## Questions?

If you have any questions about the assignment, please open an issue in the repository.
