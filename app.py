import os
from flask import Flask, render_template, flash, redirect, url_for
from flask.globals import app_ctx
from dontenv import load_dotenv
from models import db, User
from flask_login import LoginManager

from auth import auth_bp
from music import music_bp


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # Connect database to the app
    db.init_app(app)

    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.signin"
    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/users")
    app.register_blueprint(music_bp, url_prefix="/")

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    # Error handler
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("not_found.html"), 404

        if __name__ == "__main__":
            app = create_app()
            app.run(debug=True)
