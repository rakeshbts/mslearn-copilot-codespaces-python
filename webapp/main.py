
# Standard library imports
import os
import base64
import hashlib
from typing import Union
from os.path import dirname, abspath, join

# Third-party imports
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError



# Paths
current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

# FastAPI app with versioning
app = FastAPI(
    title="Token Generator & Checksum API",
    version="1.0.0",
    description="A simple API for generating tokens and checksums."
)

# CORS middleware for security and flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/ui", StaticFiles(directory=static_path), name="ui")



class TokenRequest(BaseModel):
    """Request model for token generation."""
    length: Union[int, None] = Field(20, ge=1, le=128, description="Token length (1-128)")



class ChecksumRequest(BaseModel):
    """Request model for checksum calculation."""
    text: str = Field(..., min_length=1, max_length=1000, description="Text to hash")
    hash_type: Union[str, None] = Field('sha256', description="Hash type: md5, sha1, sha256")



# API version prefix
API_PREFIX = "/api/v1"

@app.get("/", include_in_schema=False)
def root():
    """Serve the main HTML page."""
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)



@app.post(f"{API_PREFIX}/generate", response_model=dict)
def generate_token(body: TokenRequest):
    """
    Generate a pseudo-random token ID of specified length (default 20).
    """
    try:
        string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
        return {"token": string}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Token generation failed.")


@app.post(f"{API_PREFIX}/checksum", response_model=dict)
def checksum(input: ChecksumRequest):
    """
    Calculate a checksum hash for the provided text using the specified hash algorithm.
    """
    text = input.text.strip()
    hash_type = (input.hash_type or 'sha256').lower()
    if hash_type not in {'md5', 'sha1', 'sha256'}:
        raise HTTPException(
            status_code=400,
            detail="hash_type must be one of: md5, sha1, sha256."
        )
    try:
        hash_func = getattr(hashlib, hash_type)
        checksum_value = hash_func(text.encode('utf-8')).hexdigest()
        return {"checksum": checksum_value, "hash_type": hash_type}
    except Exception:
        raise HTTPException(status_code=500, detail="Checksum calculation failed.")


# Global exception handler for validation errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
