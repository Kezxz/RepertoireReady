from flask import Blueprint, render_template, request, redirect, url_for
from app.piece_logic import Piece, library

pieces_bp = Blueprint("pieces", __name__, url_prefix="/pieces")



@pieces_bp.get("/")
def pieces_home():
    return render_template("pieces_list.html", pieces = library.pieces)


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
    piece_id = len(library.pieces) + 1

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

    library.add_piece(new_piece)

    return redirect(url_for("pieces.pieces_home"))


# Delete route
@pieces_bp.post("/delete/<int:piece_id>")
def delete_piece(piece_id):
    library.delete_piece(piece_id)
    return redirect(url_for("pieces.pieces_home"))