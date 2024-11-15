import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test that the home route returns status code 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Available Jobs" in response.data  # Ensure the template renders correctly
