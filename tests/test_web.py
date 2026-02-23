import pytest
from web import create_app

@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    app = create_app()
    app.config["TESTING"] = True
    # In a real scenario, we might swap out real CSVs for temp ones here
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    """Confirm the root route returns a 200 OK and basic branding."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"RepertoireReady" in response.data

def test_pieces_list_integration(client):
    """Verify the pieces route correctly renders Abby's HTML and Parker's data."""
    response = client.get("/pieces/")
    assert response.status_code == 200
    
    # Assert Abby's styling/structure exists
    assert b'class="header"' in response.data
    assert b"Status" in response.data
    
    # Assert Parker's hardcoded logic data is passed through
    assert b"Moonlight Sonata" in response.data
    assert b"Beethoven" in response.data

def test_setlists_template_inheritance(client):
    """Verify that the setlists page correctly uses base.html inheritance."""
    response = client.get("/setlists/")
    assert response.status_code == 200
    
    # If inheritance works, the Nav bar from base.html must be present
    assert b"Home" in response.data
    assert b"Pieces" in response.data
    
    # Verify the specific setlist content
    assert b"Spring Concert" in response.data
