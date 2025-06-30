"""
Fault injection tests for the storage service.
"""
import pytest
import time
import random
import string
from unittest.mock import patch, MagicMock
from fastapi import status

class TestFaultInjection:
    """Fault injection test cases for the storage service."""
    
    def test_storage_failure_during_upload(self, test_app, sample_file):
        """Test handling of storage failure during file upload."""
        # Patch the file writing operation to fail
        with patch('src.storage_service.files_content.__setitem__', 
                 side_effect=Exception("Storage failure")):
            response = test_app.post(
                "/files",
                files={"file": (sample_file["filename"], sample_file["content"], sample_file["content_type"])}
            )
            
            # Should return 500 error
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "error" in response.json()
        
        # Verify no partial file was created
        stats = test_app.get("/admin/stats").json()
        assert stats["total_files"] == 0
    
    def test_concurrent_modification(self, test_app, upload_file):
        """Test handling of concurrent modifications to the same file."""
        file_id = upload_file["file_id"]
        
        # Simulate two concurrent updates to the same file
        def update_file():
            # Get current metadata
            metadata = test_app.get(f"/files/{file_id}/metadata").json()
            
            # Modify the file
            test_app.post(
                "/files",
                files={"file": ("concurrent_update.txt", b"new content", "text/plain")}
            )
            
            # Try to update with old metadata (simulate lost update)
            response = test_app.put(
                f"/files/{file_id}/metadata",
                json={"filename": "updated.txt", "etag": metadata["etag"]}
            )
            return response
        
        # Run multiple concurrent updates
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(update_file) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Verify at least one update was successful
        status_codes = [r.status_code for r in results]
        assert status.HTTP_200_OK in status_codes or status.HTTP_409_CONFLICT in status_codes
    
    def test_network_partition_during_tiering(self, test_app, upload_file):
        """Test behavior when network partition occurs during tiering."""
        file_id = upload_file["file_id"]
        
        # Mock the storage movement to fail after partial completion
        def failing_move(*args, **kwargs):
            # Simulate partial failure
            raise Exception("Network partition during tiering")
        
        with patch('src.storage_service.files_metadata.__setitem__', side_effect=failing_move):
            response = test_app.post("/admin/tiering/run")
            
            # Should indicate partial failure
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "partial_success"
        
        # Verify file is still accessible and in a consistent state
        response = test_app.get(f"/files/{file_id}/metadata")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["tier"] == "HOT"  # Should not have moved
    
    def test_corrupt_metadata(self, test_app, upload_file):
        """Test behavior when metadata becomes corrupted."""
        file_id = upload_file["file_id"]
        
        # Corrupt the metadata
        import src.storage_service
        src.storage_service.files_metadata[file_id] = {"invalid": "data"}
        
        # Try to access the file
        response = test_app.get(f"/files/{file_id}/metadata")
        
        # Should handle gracefully - either 500 or 404 is acceptable
        assert response.status_code in (
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            status.HTTP_404_NOT_FOUND
        )
    
    def test_slow_storage(self, test_app, monkeypatch):
        """Test behavior with slow storage backend."""
        # Add delay to storage operations
        original_setitem = dict.__setitem__
        
        def slow_setitem(d, key, value):
            time.sleep(0.1)  # 100ms delay
            return original_setitem(d, key, value)
        
        monkeypatch.setattr(dict, "__setitem__", slow_setitem)
        
        # Test upload with slow storage
        start_time = time.time()
        response = test_app.post(
            "/files",
            files={"file": ("slow.txt", b"x" * (2 * 1024 * 1024), "text/plain")}
        )
        duration = time.time() - start_time
        
        # Should still complete successfully, just slower
        assert response.status_code == status.HTTP_201_CREATED
        assert duration >= 0.1  # Should take at least 100ms
    
    def test_high_memory_usage(self, test_app):
        """Test behavior with high memory usage scenarios."""
        # Upload many large files to consume memory
        file_count = 50
        file_size = 10 * 1024 * 1024  # 10MB
        
        for i in range(file_count):
            try:
                response = test_app.post(
                    "/files",
                    files={
                        "file": (
                            f"large_{i}.bin", 
                            b"x" * file_size,
                            "application/octet-stream"
                        )
                    }
                )
                # Allow some failures due to memory pressure
                if response.status_code >= 500:
                    break
            except Exception:
                break
        
        # Verify system is still responsive
        response = test_app.get("/admin/stats")
        assert response.status_code == status.HTTP_200_OK
        
        # Clean up
        stats = response.json()
        if stats["total_files"] > 0:
            response = test_app.post("/admin/tiering/run")
            assert response.status_code == 200
