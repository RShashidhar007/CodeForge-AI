"""
Test authentication endpoints matching Java test patterns.
"""
import pytest
from fastapi.testclient import TestClient


def test_register_candidate_success(client: TestClient):
    """Test successful candidate registration."""
    response = client.post(
        "/api/auth/register/candidate",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["role"] == "CANDIDATE"
    assert data["enabled"] is True


def test_register_candidate_duplicate_email(client: TestClient):
    """Test duplicate email rejection."""
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    # First registration
    response = client.post("/api/auth/register/candidate", json=payload)
    assert response.status_code == 201
    
    # Second registration with same email
    response = client.post("/api/auth/register/candidate", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["message"].lower()


def test_login_success(client: TestClient):
    """Test successful login."""
    # Register
    client.post(
        "/api/auth/register/candidate",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token_type"] == "Bearer"
    assert data["expires_in_seconds"] > 0
    assert data["user"]["email"] == "john@example.com"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["message"].lower()


def test_register_recruiter_success(client: TestClient):
    """Test successful recruiter registration without company."""
    response = client.post(
        "/api/auth/register/recruiter",
        json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "password123",
            "designation": "Senior Recruiter"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "jane@example.com"
    assert data["role"] == "RECRUITER"
