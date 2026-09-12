"""
Test candidate endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_candidate_can_access_profile(client: TestClient):
    """Test that candidate can access their own profile."""
    # Register and login
    client.post(
        "/api/auth/register/candidate",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
    )
    login_response = client.post(
        "/api/auth/login",
        json={"email": "john@example.com", "password": "password123"}
    )
    token = login_response.json()["token"]
    
    # Get profile
    response = client.get(
        "/api/candidates/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["skills"] == []


def test_candidate_can_update_profile(client: TestClient):
    """Test that candidate can update their profile."""
    # Register and login
    client.post(
        "/api/auth/register/candidate",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
    )
    login_response = client.post(
        "/api/auth/login",
        json={"email": "john@example.com", "password": "password123"}
    )
    token = login_response.json()["token"]
    
    # Update profile
    response = client.put(
        "/api/candidates/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+1234567890",
            "location": "San Francisco",
            "bio": "Software engineer",
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "github_url": "https://github.com/johndoe"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+1234567890"
    assert data["location"] == "San Francisco"
    assert len(data["skills"]) == 3


def test_recruiter_cannot_access_candidate_endpoint(client: TestClient):
    """Test that recruiter cannot access candidate endpoints."""
    # Register recruiter and login
    client.post(
        "/api/auth/register/recruiter",
        json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "password123"
        }
    )
    login_response = client.post(
        "/api/auth/login",
        json={"email": "jane@example.com", "password": "password123"}
    )
    token = login_response.json()["token"]
    
    # Try to access candidate endpoint
    response = client.get(
        "/api/candidates/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
