from flask import Blueprint

setlists_bp = Blueprint("setlists", __name__, url_prefix="/setlists")


@setlists_bp.get("/")
def setlists_home():

    # Placeholder

    return (
        "<h2>Setlists</h2>"
        "<p>Placeholder page.</p>"
        '<p><a href="/">Back to Home</a></p>'
    )