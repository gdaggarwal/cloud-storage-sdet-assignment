"""
Mock Storage Service for Cloud Storage Tiering System
"""
import os
import uuid
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional, List, Tuple
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Cloud Storage Tiering Service")

class StorageTier(str, Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"

class FileMetadata(BaseModel):
    file_id: str
    filename: str
    size: int
    tier: StorageTier
    created_at: datetime
    last_accessed: datetime
    content_type: str
    etag: str

class StorageStats(BaseModel):
    total_files: int
    total_size: int
    tiers: Dict[str, Dict[str, int]]

# In-memory storage for demo purposes
files_metadata: Dict[str, FileMetadata] = {}
files_content: Dict[str, bytes] = {}

# Tier configuration
TIER_CONFIG = {
    StorageTier.HOT: {
        "max_age_days": 30,
        "next_tier": StorageTier.WARM,
        "size_limit": 10 * 1024 * 1024 * 1024  # 10GB
    },
    StorageTier.WARM: {
        "max_age_days": 90,
        "next_tier": StorageTier.COLD,
        "size_limit": 100 * 1024 * 1024 * 1024  # 100GB
    },
    StorageTier.COLD: {
        "max_age_days": None,  # No automatic movement from COLD
        "next_tier": None,
        "size_limit": 1024 * 1024 * 1024 * 1024  # 1TB
    }
}

@app.post("/files", response_model=FileMetadata, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """Upload a new file to the storage service."""
    file_id = str(uuid.uuid4())
    content = await file.read()
    
    # Basic validation
    if len(content) < 1024 * 1024:  # 1MB minimum
        raise HTTPException(status_code=400, detail="File size must be at least 1MB")
    if len(content) > 10 * 1024 * 1024 * 1024:  # 10GB maximum
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 10GB")
    
    now = datetime.utcnow()
    metadata = FileMetadata(
        file_id=file_id,
        filename=file.filename,
        size=len(content),
        tier=StorageTier.HOT,
        created_at=now,
        last_accessed=now,
        content_type=file.content_type or "application/octet-stream",
        etag=str(uuid.uuid4())
    )
    
    files_metadata[file_id] = metadata
    files_content[file_id] = content
    
    return metadata

@app.get("/files/{file_id}")
async def download_file(file_id: str):
    """Download a file by its ID."""
    if file_id not in files_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    metadata = files_metadata[file_id]
    metadata.last_accessed = datetime.utcnow()
    
    return {
        "content": files_content[file_id],
        "filename": metadata.filename,
        "content_type": metadata.content_type
    }

@app.get("/files/{file_id}/metadata", response_model=FileMetadata)
async def get_file_metadata(file_id: str):
    """Get metadata for a file."""
    if file_id not in files_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return files_metadata[file_id]

@app.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: str):
    """Delete a file."""
    if file_id not in files_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    files_metadata.pop(file_id, None)
    files_content.pop(file_id, None)
    
    return None

@app.post("/admin/tiering/run")
async def run_tiering():
    """Run the tiering process to move files between storage tiers."""
    moved_count = 0
    now = datetime.utcnow()
    
    for file_id, metadata in list(files_metadata.items()):
        tier_config = TIER_CONFIG[metadata.tier]
        
        # Skip if this is the coldest tier or no next tier defined
        if not tier_config["next_tier"]:
            continue
        
        # Check if file should be moved to next tier
        days_since_access = (now - metadata.last_accessed).days
        if days_since_access >= tier_config["max_age_days"]:
            metadata.tier = tier_config["next_tier"]
            moved_count += 1
    
    return {"status": "success", "files_moved": moved_count}

class UpdateLastAccessedRequest(BaseModel):
    days_ago: int

@app.post("/admin/files/{file_id}/update-last-accessed")
async def update_last_accessed(file_id: str, request: UpdateLastAccessedRequest):
    """Update the last_accessed time of a file (for testing purposes)."""
    if file_id not in files_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Update last_accessed to be X days ago
    files_metadata[file_id].last_accessed = datetime.utcnow() - timedelta(days=request.days_ago)
    return {
        "status": "success", 
        "file_id": file_id, 
        "last_accessed": files_metadata[file_id].last_accessed.isoformat()
    }

@app.get("/admin/stats")
async def get_stats():
    """Get storage statistics."""
    stats = {
        "total_files": len(files_metadata),
        "total_size": sum(m.size for m in files_metadata.values()),
        "tiers": {
            tier: {"count": 0, "size": 0}
            for tier in StorageTier
        }
    }
    
    for metadata in files_metadata.values():
        stats["tiers"][metadata.tier]["count"] += 1
        stats["tiers"][metadata.tier]["size"] += metadata.size
    
    return stats

def start_service():
    """Start the storage service."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_service()
