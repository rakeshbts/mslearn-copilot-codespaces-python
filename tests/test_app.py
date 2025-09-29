"""
Unit and integration tests for the FastAPI application.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure the app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../webapp')))
from main import app

client = TestClient(app)

API_PREFIX = "/api/v1"

def test_generate_token_default():
    response = client.post(f"{API_PREFIX}/generate", json={})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) == 20

def test_generate_token_custom_length():
    response = client.post(f"{API_PREFIX}/generate", json={"length": 32})
    assert response.status_code == 200
    data = response.json()
    assert len(data["token"]) == 32

def test_generate_token_invalid_length():
    response = client.post(f"{API_PREFIX}/generate", json={"length": 0})
    assert response.status_code == 422

def test_checksum_sha256():
    response = client.post(f"{API_PREFIX}/checksum", json={"text": "hello world"})
    assert response.status_code == 200
    data = response.json()
    assert data["hash_type"] == "sha256"
    assert data["checksum"] == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

def test_checksum_md5():
    response = client.post(f"{API_PREFIX}/checksum", json={"text": "hello world", "hash_type": "md5"})
    assert response.status_code == 200
    data = response.json()
    assert data["hash_type"] == "md5"
    assert data["checksum"] == "5eb63bbbe01eeed093cb22bb8f5acdc3"

def test_checksum_sha1():
    response = client.post(f"{API_PREFIX}/checksum", json={"text": "hello world", "hash_type": "sha1"})
    assert response.status_code == 200
    data = response.json()
    assert data["hash_type"] == "sha1"
    assert data["checksum"] == "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"

def test_checksum_invalid_hash_type():
    response = client.post(f"{API_PREFIX}/checksum", json={"text": "hello world", "hash_type": "invalid"})
    assert response.status_code == 400
    assert "hash_type must be one of" in response.text

def test_checksum_empty_text():
    response = client.post(f"{API_PREFIX}/checksum", json={"text": ""})
    assert response.status_code == 422

def test_checksum_text_too_long():
    long_text = "a" * 1001
    response = client.post(f"{API_PREFIX}/checksum", json={"text": long_text})
    assert response.status_code == 422
