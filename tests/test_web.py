import pytest
from web import create_app
from app.piece_logic import library, Piece

@pytest.fixture
def client():
    """Provides a fresh, isolated test client for every test case."""
    app = create_app()
    app.config.update({"TESTING": True})
    
    # Clear the shared library state to ensure test independence
    library.pieces = [] 
    
    with app.test_client() as client:
        yield client

def test_branding_and_navigation(client):
    """Verify core branding and navigation are present on the landing page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"RepertoireReady" in response.data
    assert b"Pieces" in response.data

def test_add_piece_functional_flow(client):
    """Verify that submitting the web form adds data to the backend logic."""
    # Data keys match Parker's request.form.get keys in pieces_routes.py
    form_payload = {
        "title": "Sonata in C",
        "composer": "Mozart",
        "genre": "Classical",
        "readiness_status": "learning"
    }
    # Act: Submit form and follow the redirect back to the list
    response = client.post("/pieces/form", data=form_payload, follow_redirects=True)
    
    # Assert: Check UI and Logic state
    assert response.status_code == 200
    assert b"Sonata in C" in response.data
    assert len(library.pieces) == 1
    assert library.pieces[0].composer == "Mozart"

def test_delete_piece_functional_flow(client):
    """Verify that the delete action removes the piece from the UI and Library."""
    # Arrange: Add a piece to delete
    library.add_piece(Piece(1, "Delete Me", "N/A", "N/A", "learning", 1))
    
    # Act: Post to Parker's delete route
    response = client.post("/pieces/delete/1", follow_redirects=True)
    
    # Assert: Verify removal
    assert b"Delete Me" not in response.data
    assert len(library.pieces) == 0

def test_setlist_data_persistence(client):
    """Verify the setlists page displays the performance data."""
    response = client.get("/setlists/")
    assert b"Spring Concert" in response.data
    assert b"Jazz Showcase" in response.data
