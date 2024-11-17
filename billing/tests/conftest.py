import pytest
from billing import create_app

@pytest.fixture
def app():
    """Fixture for creating the Flask app in test mode."""
    app = create_app()
    app.config['TESTING'] = True  # Enable Flask testing mode
    app.config['MYSQL_DB'] = "test_billing_db"  # Use a test database
    yield app

@pytest.fixture
def client(app):
    """Fixture for creating a test client for the app."""
    return app.test_client()
