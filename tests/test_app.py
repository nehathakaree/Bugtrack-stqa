import pytest
from app import app, db, User
from werkzeug.security import generate_password_hash

@pytest.fixture()
def client():
    app.config.update(TESTING=True, SECRET_KEY="test-secret", SQLALCHEMY_DATABASE_URI="sqlite://")
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(User(name="Test User", email="test@example.com", password_hash=generate_password_hash("correct-horse")))
        db.session.commit()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_home_page(client):
    assert client.get("/").status_code == 200

def test_dashboard_requires_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302 and "/login" in response.location

def test_valid_login(client):
    response = client.post("/login", data={"email":"test@example.com","password":"correct-horse"}, follow_redirects=True)
    assert response.status_code == 200 and b"Quality dashboard" in response.data

def test_invalid_login(client):
    response = client.post("/login", data={"email":"test@example.com","password":"wrong"}, follow_redirects=True)
    assert b"Invalid email or password" in response.data

def test_register_short_password(client):
    response = client.post("/register", data={"name":"New","email":"new@example.com","password":"123"}, follow_redirects=True)
    assert b"at least 8 characters" in response.data
