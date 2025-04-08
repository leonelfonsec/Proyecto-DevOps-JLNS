import pytest
from unittest.mock import patch, MagicMock
from app.models import BlacklistEntry
from app.schemas import BlacklistSchema
from app.routes import STATIC_TOKEN
from faker import Faker
from app import create_app

fake = Faker()

@pytest.fixture
def client():
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = "test-secret"

    app = create_app(TestConfig)

    with patch("app.models.BlacklistEntry") as MockEntry:
        with app.test_client() as client:
            yield client

def auth_header():
    return {"Authorization": f"Bearer {STATIC_TOKEN}"}

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

@patch("app.routes.db.session")
@patch("app.routes.BlacklistEntry")
def test_post_blacklist_valid(mock_blacklist_entry, mock_session, client):
    payload = {
        "email": fake.email(),
        "app_uuid": fake.uuid4(),
        "blocked_reason": fake.sentence(nb_words=3)
    }
    mock_instance = MagicMock()
    mock_blacklist_entry.return_value = mock_instance

    response = client.post("/blacklists", json=payload, headers=auth_header())

    assert response.status_code == 201
    assert response.get_json() == {"message": "Email added to blacklist"}
    assert mock_session.add.called
    assert mock_session.commit.called

@patch("app.routes.db.session")
def test_post_blacklist_invalid_payload(mock_session, client):
    payload = {
        "app_uuid": fake.uuid4()
    }
    response = client.post("/blacklists", json=payload, headers=auth_header())
    assert response.status_code == 400
    assert "errors" in response.get_json()

@patch("app.routes.BlacklistEntry.query")
def test_check_blacklisted_email(mock_query, client):
    mock_entry = MagicMock()
    mock_entry.blocked_reason = fake.sentence(nb_words=2)
    mock_query.filter_by.return_value.first.return_value = mock_entry

    email = fake.email()
    response = client.get(f"/blacklists/{email}", headers=auth_header())
    assert response.status_code == 200
    assert response.get_json() == {"blacklisted": True, "reason": mock_entry.blocked_reason}

@patch("app.routes.BlacklistEntry.query")
def test_check_non_blacklisted_email(mock_query, client):
    mock_query.filter_by.return_value.first.return_value = None

    email = fake.email()
    response = client.get(f"/blacklists/{email}", headers=auth_header())
    assert response.status_code == 200
    assert response.get_json() == {"blacklisted": False}
