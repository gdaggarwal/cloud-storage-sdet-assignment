"""
Test configuration and fixtures for the storage service tests.
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from src.storage_service import app, files_metadata, files_content

@pytest.fixture(scope="module")
def test_app():
    """
    Create a test client for the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def reset_storage():
    """
    Reset the storage state before each test.
    """
    files_metadata.clear()
    files_content.clear()

@pytest.fixture
def sample_file():
    """
    Create a sample file for testing.
    """
    return {
        "filename": "test.txt",
        "content": b"This is a test file" * 1024 * 1024,  # ~2MB
        "content_type": "text/plain"
    }

@pytest.fixture
def upload_file(test_app, sample_file):
    """
    Upload a sample file and return its metadata.
    """
    response = test_app.post(
        "/files",
        files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
    )
    return response.json()
