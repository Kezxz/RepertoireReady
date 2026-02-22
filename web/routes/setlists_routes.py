from flask import Blueprint, render_template
from app.setlist_logic import Performance

setlists_bp = Blueprint("setlists", __name__, url_prefix="/setlists")

setlists = [
    Performance(1, "Spring Concert", "2026-03-10", "Auditorium", 101),
    Performance(2, "Anime Club Night", "2026-03-21", "Room 204", 101),
    Performance(3, "Jazz Showcase", "2026-04-05", "Main Hall", 102),
]

@setlists_bp.get("/")
def setlists_home():
    return render_template("setlists_list.html", setlists=setlists)