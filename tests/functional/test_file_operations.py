"""
Functional tests for file operations in the storage service.
"""
import pytest
from datetime import datetime, timedelta
from fastapi import status

class TestFileOperations:
    """Test cases for file operations."""
    
    def test_upload_file(self, test_app, sample_file):
        """Test uploading a file."""
        response = test_app.post(
            "/files",
            files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["filename"] == sample_file["filename"]
        assert data["size"] == len(sample_file["content"])
        assert data["tier"] == "HOT"
        assert "file_id" in data
    
    def test_upload_file_too_small(self, test_app):
        """Test uploading a file that's too small."""
        small_content = b"x" * (1024 * 1024 - 1)  # 1 byte less than 1MB
        response = test_app.post(
            "/files",
            files={"file": ("small.txt", small_content, "text/plain")}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "File size must be at least 1MB" in response.text
    
    def test_download_file(self, test_app, sample_file):
        """Test downloading a file."""
        # First upload a file
        upload_response = test_app.post(
            "/files",
            files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
        )
        assert upload_response.status_code == status.HTTP_201_CREATED
        file_data = upload_response.json()
        file_id = file_data["file_id"]
        
        # Then download it
        response = test_app.get(f"/files/{file_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # The response should be a JSON with the file content and metadata fields directly
        response_data = response.json()
        assert "content" in response_data
        assert "content_type" in response_data
        assert "filename" in response_data
        assert response_data["content"] == sample_file["content"].decode()
    
    def test_download_nonexistent_file(self, test_app):
        """Test downloading a file that doesn't exist."""
        response = test_app.get("/files/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_metadata(self, test_app, sample_file):
        """Test getting file metadata."""
        # First upload a file
        upload_response = test_app.post(
            "/files",
            files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
        )
        assert upload_response.status_code == status.HTTP_201_CREATED
        file_data = upload_response.json()
        file_id = file_data["file_id"]
        
        # Then get its metadata
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["file_id"] == file_id
        assert data["filename"] == sample_file["filename"]
        assert data["size"] == len(sample_file["content"])
    
    def test_delete_file(self, test_app, upload_file):
        """Test deleting a file."""
        file_id = upload_file["file_id"]
        
        # Verify file exists
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_200_OK
        
        # Delete the file
        response = test_app.delete(f"/files/{file_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify file no longer exists
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_404_NOT_FOUND

class TestTieringOperations:
    """Test cases for storage tiering operations."""
    
    def test_tiering_process(self, test_app, sample_file, monkeypatch):
        """Test the tiering process moves files between tiers."""
        # Upload a file first
        upload_response = test_app.post(
            "/files",
            files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
        )
        assert upload_response.status_code == status.HTTP_201_CREATED
        file_data = upload_response.json()
        file_id = file_data["file_id"]
        
        # Initially in HOT tier
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["tier"] == "HOT"
        
        # Use admin endpoint to update last_accessed time to 31 days ago
        update_response = test_app.post(
            f"/admin/files/{file_id}/update-last-accessed",
            json={"days_ago": 31}
        )
        assert update_response.status_code == status.HTTP_200_OK
        
        # Run tiering process
        response = test_app.post("/admin/tiering/run")
        assert response.status_code == status.HTTP_200_OK
        
        # Check if the file was moved to WARM tier
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["tier"] == "WARM"
    
    def test_tiering_multiple_files(self, test_app, sample_file, monkeypatch):
        """Test tiering with multiple files."""
        # Upload multiple files
        file_ids = []
        for i in range(3):
            response = test_app.post(
                "/files",
                files={"file": (f"file_{i}.txt", sample_file["content"], "text/plain")}
            )
            assert response.status_code == status.HTTP_201_CREATED
            file_data = response.json()
            file_ids.append(file_data["file_id"])
        
        # Set different last_accessed times to trigger different tiering
        # Using thresholds that match the TIER_CONFIG in storage_service.py:
        # - HOT -> WARM: after 30 days
        # - WARM -> COLD: after 90 days
        # - COLD: no automatic movement
        test_cases = [
            (30, "WARM"),   # 30 days old -> WARM
            (60, "WARM"),   # 60 days old -> still WARM (needs 90+ days to go to COLD)
            (120, "COLD")   # 120 days old -> COLD
        ]
        
        for i, (days_ago, expected_tier) in enumerate(test_cases):
            file_id = file_ids[i]
            update_response = test_app.post(
                f"/admin/files/{file_id}/update-last-accessed",
                json={"days_ago": days_ago}
            )
            assert update_response.status_code == status.HTTP_200_OK
        
        # Run tiering process multiple times to allow for multi-tier transitions
        # First run: Move from HOT to WARM for files older than 30 days
        response = test_app.post("/admin/tiering/run")
        assert response.status_code == status.HTTP_200_OK
        
        # Second run: Move from WARM to COLD for files older than 90 days
        response = test_app.post("/admin/tiering/run")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify files are in correct tiers based on their age
        for i, (days_ago, expected_tier) in enumerate(test_cases):
            file_id = file_ids[i]
            response = test_app.get(f"/files/{file_id}/metadata")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["tier"] == expected_tier, f"File {i+1} with {days_ago} days should be in {expected_tier} tier"
