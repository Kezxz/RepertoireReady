from flask import Blueprint, render_template
from app.piece_logic import PieceLibrary, Piece

pieces_bp = Blueprint("pieces", __name__, url_prefix="/pieces")


# Below can be deleted later. It's for testing
library = PieceLibrary()
library.add_piece(Piece(1, "Moonlight Sonata", "Beethoven", "Classical", "In Progress", 101))
library.add_piece(Piece(2, "Clair de Lune", "Debussy", "Classical", "Ready", 102))
library.add_piece(Piece(3, "Nocturne in E-flat Major", "Chopin", "Classical", "In Progress", 103))
library.add_piece(Piece(4, "The Four Seasons", "Vivaldi", "Classical", "Ready", 104))



@pieces_bp.get("/")
def pieces_home():

    # Placeholder

    return render_template("pieces_list.html", pieces = library.pieces)