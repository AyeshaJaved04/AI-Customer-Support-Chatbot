def test_health(client):
    """Health endpoint should return status healthy"""
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_register_new_user(client):
    """Should register a new user and return 201"""
    r = client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "name": "New User",
        "password": "newpass123"
    })
    assert r.status_code == 201
    assert r.json()["email"] == "newuser@test.com"

def test_register_duplicate(client):
    """Should reject duplicate email with 400"""
    client.post("/api/v1/auth/register", json={
        "email": "duplicate@test.com",
        "name": "Dup User",
        "password": "testpass123"
    })
    r = client.post("/api/v1/auth/register", json={
        "email": "duplicate@test.com",
        "name": "Dup User 2",
        "password": "testpass123"
    })
    assert r.status_code == 400

def test_login_success(client):
    """Should return access token on valid login"""
    r = client.post("/api/v1/auth/login",
        data={"username": "test@test.com", "password": "testpass123"})
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password(client):
    """Should return 401 on wrong password"""
    r = client.post("/api/v1/auth/login",
        data={"username": "test@test.com", "password": "wrongpass"})
    assert r.status_code == 401

def test_chat_requires_auth(client):
    """Chat endpoint should require authentication"""
    r = client.post("/api/v1/chat",
        json={"user_id": 1, "message": "hello"})
    assert r.status_code == 401

def test_history_requires_auth(client):
    """History endpoint should require authentication"""
    r = client.get("/api/v1/users/1/history")
    assert r.status_code == 401

def test_tickets_requires_auth(client):
    """Tickets endpoint should require authentication"""
    r = client.get("/api/v1/users/1/tickets")
    assert r.status_code == 401