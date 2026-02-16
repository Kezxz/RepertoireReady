import pytest
from app import piece_logic as pl
from datetime import date


def test_add_piece_sets_created_date():
    #Arrange
    library = pl.PieceLibrary()
    piece = pl.Piece(
        piece_id= 1,
        title= "Fir Elise",
        composer= "Beethoven",
        genre= "Classical",
        readiness_status= "In progess",
        user_id= 101
    )

    # Act
    library.add_piece(piece)


    # Assert
    assert len(library.pieces) == 1
    assert library.pieces[0] == piece
    assert piece.created == date.today()




def test_edit_piece_adds_updated_time():
    # Arrange 
    library = pl.PieceLibrary()
    piece = pl.Piece(
        piece_id = 1,
        title = "Old Title",
        composer = "Old Composer",
        genre = "Classical",
        readiness_status = "Not Ready",
        user_id = 101
    )

    library.add_piece(piece)

    # Act
    result = library.edit_piece(
        piece_id = 1,
        new_title = "New Title",
        new_composer = "New Composer",
        new_genre= "Jazz",
        new_readiness_status= "In Progress",
    )


    # Assert
    assert result is True
    assert piece.title == "New Title"
    assert piece.composer == "New Composer"
    assert piece.genre == "Jazz"
    assert piece.readiness_status == "In Progress"
    assert piece.updated == date.today()



def test_delete_piece_and_return_if_not_found():
    library = pl.PieceLibrary()
    piece1 = pl.Piece(
        piece_id = 1,
        title = "Piece 1",
        composer = "Composer 1",
        genre = "Classical",
        readiness_status = "Ready",
        user_id = 101
    )

    piece2 = pl.Piece(
        piece_id = 2,
        title= "Piece 2",
        composer= "Composer 2",
        genre= "Jazz",
        readiness_status= "In Progress",
        user_id= 102
    )

    library.add_piece(piece1)
    library.add_piece(piece2)


    # Act and Assert
    # Deleting an existing piece
    result = library.delete_piece(piece_id=1)
    assert result is True
    assert len(library.pieces) == 1
    assert library.pieces[0].piece_id == 2

    # Trying to delete a non-existent piece
    result_nonexistent = library.delete_piece(piece_id=3)
    assert result_nonexistent is False
    assert len(library.pieces) == 1 # library unchanged