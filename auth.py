from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint("auth", __name__)


# Sign up route
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("music.home"))

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Validating input
        if not username or not password:
            flash("Username and password required.", "error")
            return redirect(url_for("auth.signup"))

        # Checking for duplicate username
        existing_user = db.session.scalar(
            db.select(User).where(User.username == username)
        )

        if existing_user:
            flash("User with that name already exists.", "error")
            return redirect(url_for("auth.signup"))

        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registered! Please sign in.", "success")
        return redirect(url_for("auth.signin"))

    return render_template("signup.html")


# Sign in route
@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("music.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Find user
        user = db.session.scalar(db.select(User).where(User.username == username))

        # Check password
        if user is None or not user.check_password(password):
            flash("Invalid credentials.", "error")
            return redirect(url_for("auth.signin"))

        # Log in user
        login_user(user)
        flash("Welcome to MusicTracker!", "success")
        return redirect(url_for("music.home"))
    return render_template("signin.html")


# Sign out route
@auth_bp.route("/signout", methods=["POST"])
@login_required
def signout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("music.home"))
