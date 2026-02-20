from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    from .routes.pieces_routes import pieces_bp
    from .routes.setlists_routes import setlists_bp

    app.register_blueprint(pieces_bp)
    app.register_blueprint(setlists_bp)

    @app.get("/")
    def home():
        return (
            '<h1>RepertoireReady</h1>'
            '<ul>'
            '<li><a href="/pieces">Pieces</a></li>'
            '<li><a href="/setlists">Setlists</a></li>'
            "</ul>"
        )

    return app