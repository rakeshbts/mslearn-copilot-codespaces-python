"""
API routes for token generation and checksum calculation.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, ValidationError
import base64
import os
import hashlib

router = APIRouter()

class TokenRequest(BaseModel):
    length: Optional[int] = Field(20, ge=1, le=128, description="Token length (1-128)")

    class Config:
        schema_extra = {
            "example": {"length": 20}
        }

class ChecksumRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to hash")
    hash_type: Optional[str] = Field('sha256', description="Hash type: md5, sha1, sha256")

    class Config:
        schema_extra = {
            "example": {"text": "hello world", "hash_type": "md5"}
        }

@router.post('/generate', response_model=dict)
async def generate_token(body: TokenRequest) -> dict:
    """
    Generate a pseudo-random token ID of specified length (default 20).
    """
    try:
        string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
        return {"token": string}
    except Exception:
        raise HTTPException(status_code=500, detail="Token generation failed.")

@router.post('/checksum', response_model=dict)
async def checksum(input: ChecksumRequest) -> dict:
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
