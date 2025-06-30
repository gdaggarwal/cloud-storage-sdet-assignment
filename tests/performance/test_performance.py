"""
Performance tests for the storage service.
"""
import pytest
import time
from datetime import datetime, timedelta

class TestPerformance:
    """Performance test cases for the storage service."""
    
    @pytest.mark.parametrize("file_size_mb", [1, 10, 100])
    def test_upload_performance(self, test_app, benchmark, file_size_mb):
        """Test upload performance with different file sizes."""
        # Generate test file content (1MB chunks)
        content = b"x" * (1024 * 1024 * file_size_mb)
        
        def upload():
            response = test_app.post(
                "/files",
                files={"file": (f"test_{file_size_mb}mb.bin", content, "application/octet-stream")}
            )
            assert response.status_code == 201
            return response.json()
        
        # Warm-up
        upload()
        
        # Benchmark
        result = benchmark(upload)
        
        # Basic assertions
        assert "file_id" in result
        assert result["size"] == len(content)
    
    def test_concurrent_uploads(self, test_app):
        """Test handling of concurrent file uploads."""
        import concurrent.futures
        
        file_count = 10
        file_size = 5 * 1024 * 1024  # 5MB
        content = b"x" * file_size
        
        def upload_file(i):
            response = test_app.post(
                "/files",
                files={"file": (f"concurrent_{i}.bin", content, "application/octet-stream")}
            )
            return response.status_code == 201
        
        # Execute uploads in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(upload_file, range(file_count)))
        
        # Verify all uploads succeeded
        assert all(results)
        
        # Verify all files exist
        stats = test_app.get("/admin/stats").json()
        assert stats["total_files"] == file_count
    
    def test_tiering_performance(self, test_app, benchmark):
        """Test the performance of the tiering process.
        
        This test creates a large number of files and measures how long it takes
        to run the tiering process.
        """
        # Create many small files
        file_count = 100
        content = b"x" * (2 * 1024 * 1024)  # 2MB files
        
        for i in range(file_count):
            response = test_app.post(
                "/files",
                files={"file": (f"perf_{i}.bin", content, "application/octet-stream")}
            )
            assert response.status_code == 201
        
        # Define the tiering function to benchmark
        def run_tiering():
            response = test_app.post("/admin/tiering/run")
            assert response.status_code == 200
            return response.json()
        
        # Run benchmark
        result = benchmark(run_tiering)
        
        # Verify some basic properties
        assert "files_moved" in result
        assert 0 <= result["files_moved"] <= file_count
    
    def test_mixed_workload(self, test_app):
        """Test a mixed workload of uploads, downloads, and tiering."""
        import random
        import time
        
        operations = 50
        file_size = 2 * 1024 * 1024  # 2MB
        content = b"x" * file_size
        file_ids = []
        
        start_time = time.time()
        
        for i in range(operations):
            op_type = random.choice(["upload", "download", "metadata", "tiering"])
            
            if op_type == "upload" and len(file_ids) < 20:  # Limit max files
                response = test_app.post(
                    "/files",
                    files={"file": (f"mixed_{i}.bin", content, "application/octet-stream")}
                )
                if response.status_code == 201:
                    file_ids.append(response.json()["file_id"])
            
            elif op_type == "download" and file_ids:
                file_id = random.choice(file_ids)
                response = test_app.get(f"/files/{file_id}")
                assert response.status_code in (200, 404)  # 404 if file was deleted
            
            elif op_type == "metadata" and file_ids:
                file_id = random.choice(file_ids)
                response = test_app.get(f"/files/{file_id}/metadata")
                assert response.status_code in (200, 404)
            
            elif op_type == "tiering":
                response = test_app.post("/admin/tiering/run")
                assert response.status_code == 200
        
        duration = time.time() - start_time
        print(f"Completed {operations} operations in {duration:.2f} seconds")
        
        # Verify system is still in a good state
        stats = test_app.get("/admin/stats").json()
        assert stats["total_files"] == len(file_ids)
        
        # Clean up
        for file_id in file_ids:
            test_app.delete(f"/files/{file_id}")
        
        # Verify all files were deleted
        stats = test_app.get("/admin/stats").json()
        assert stats["total_files"] == 0
