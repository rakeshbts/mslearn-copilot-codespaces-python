
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

# Import and include API router
from webapp.api.routes import router as api_router
app.include_router(api_router, prefix="/api/v1")


# Serve the main HTML page
@app.get("/", include_in_schema=False)
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)
