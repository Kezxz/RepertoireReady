from flask import Blueprint

pieces_bp = Blueprint("pieces", __name__, url_prefix="/pieces")


@pieces_bp.get("/")
def pieces_home():

    # Placeholder

    return (
        "<h2>Pieces</h2>"
        "<p>Placeholder page.</p>"
        '<p><a href="/">Back to Home</a></p>'
    )