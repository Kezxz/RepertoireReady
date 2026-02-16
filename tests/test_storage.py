import pytest
import os
import csv
from app import storage
from app import piece_logic as tpl
from app import setlist_logic as sl
from datetime import date

@pytest.fixture
def temp_files(tmp_path):
    """Creates temporary paths for pieces and setlists to avoid touching real data."""
    p_path = tmp_path / "pieces.csv"
    s_path = tmp_path / "setlists.csv"
    return str(p_path), str(s_path)

def test_pieces_save_load_persistence(temp_files):
    p_path, _ = temp_files
    # 1. Arrange
    # Create a piece - logic sets .created as a date object
    p = tpl.Piece(piece_id=1, title="Nocturne", composer="Chopin", 
                  genre="Classical", readiness_status="learning", user_id=0)
    p.created = date.today()
    
    # 2. Act
    storage.save_pieces([p], path=p_path)
    loaded_pieces = storage.load_pieces(path=p_path)
    
    # 3. Assert
    assert len(loaded_pieces) == 1
    assert loaded_pieces[0].title == "Nocturne"
    # Confirming known behavior: Date object becomes a String after loading
    assert isinstance(loaded_pieces[0].created, str)
    assert loaded_pieces[0].created == str(date.today())

def test_setlist_ordering_and_reconstruction(temp_files):
    _, s_path = temp_files
    # 1. Arrange
    perf = sl.Performance(10, "Recital", "2026-05-01", "Concert Hall", 0)
    perfs = {10: perf}
    items = [
        sl.Setlist_Item(1, 10, 101, 1), # Piece 101 first
        sl.Setlist_Item(2, 10, 102, 2)  # Piece 102 second
    ]
    
    # 2. Act
    storage.save_setlists(perfs, items, path=s_path)
    loaded_perfs, loaded_items = storage.load_setlists(path=s_path)
    
    # 3. Assert
    assert 10 in loaded_perfs
    assert len(loaded_items) == 2
    # Verify order is preserved
    assert loaded_items[0].piece_id == 101
    assert loaded_items[1].piece_id == 102

def test_storage_creates_file_if_missing(tmp_path):
    # Verify your _ensure_parent and automatic header creation logic
    new_dir = tmp_path / "new_data"
    missing_path = str(new_dir / "auto_gen.csv")
    
    # Act
    # This should trigger the code that creates a new file with headers
    pieces = storage.load_pieces(path=missing_path)
    
    # Assert
    assert pieces == []
    assert os.path.exists(missing_path)
    with open(missing_path, 'r') as f:
        header = f.readline()
        assert "piece_id" in header
