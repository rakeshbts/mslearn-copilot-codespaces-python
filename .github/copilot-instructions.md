# Project Guidelines

## Project Overview

This repository contains a FastAPI application that provides various endpoints for token generation, text echo, and checksum calculation. 

## Technology Stack
-  **Token Generation** - An endpoint that generates secure random tokens with configurable length.
- **Text Echo** - A simple endpoint that echoes back any text sent to it.
- **Checksum Calculation** - An endpoint that calculates cryptographic hashes (SHA-256, SHA-512, or MD5) for provided text.
- **Health Checking** - A monitoring endpoint that returns the API status and version.

### ✨ Coding Style
- Follow **PEP 8** standards for formatting and naming.
- Use **type hints** consistently across all functions.
- Prefer **f-strings** for string interpolation.
- Include **Google-style docstrings** for all public functions and classes.

### 🧪 Testing Guidance
- Use **pytest** for writing unit tests.
- Mock external dependencies using `pytest-mock`.
- Name tests descriptively, e.g., `test_generate_token_valid_input`.

### 🏗️ Architecture Preferences
- Use **FastAPI** conventions for routing and dependency injection.
- Define **Pydantic models** for request and response schemas.
- Keep logic modular—separate API routes, models, and utility functions.

### 📚 Documentation & Comments
- Generate concise inline comments for non-obvious logic.
- Include endpoint descriptions in FastAPI route docstrings.
- Avoid redundant comments that restate code behavior.