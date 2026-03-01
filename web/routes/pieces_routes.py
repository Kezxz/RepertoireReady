from flask import Blueprint, render_template, request, redirect, url_for
from app.piece_logic import Piece
from app.storage import load_pieces, save_pieces
from datetime import date

pieces_bp = Blueprint("pieces", __name__, url_prefix="/pieces")


# load piece from data
@pieces_bp.get("/")
def pieces_home():
    pieces = load_pieces()
    return render_template("pieces_list.html", pieces = pieces)


# Show form
@pieces_bp.get("/form")
def pieces_form():
    return render_template("pieces_form.html")

# Handle form submission
@pieces_bp.post("/form")
def add_piece():
    
    title = request.form.get("title")
    composer = request.form.get("composer")
    genre = request.form.get("genre")
    readiness_status = request.form.get("readiness_status")

    #Auto generate piece_id
    pieces = load_pieces()
    piece_id = max([p.piece_id for p in pieces], default = 0) + 1

    # Temporary user_id
    user_id = 1

    new_piece = Piece(
        piece_id,
        title,
        composer,
        genre,
        readiness_status,
        user_id
    )

    # timestamp piece and add to list
    new_piece.created = date.today()
    pieces.append(new_piece)
    save_pieces(pieces)

    return redirect(url_for("pieces.pieces_home"))


# Delete route
@pieces_bp.post("/delete/<int:piece_id>")
def delete_piece(piece_id):
    pieces = load_pieces()
    pieces = [p for p in pieces if p.piece_id != piece_id]
    save_pieces(pieces)
    return redirect(url_for("pieces.pieces_home"))