import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from psycopg import errors

from db import query, transaction

bp = Blueprint("auth", __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped


@bp.before_app_request
def load_logged_in_user():
    if "user_id" in session:
        g.user = {"user_id": session["user_id"], "username": session["username"]}
    else:
        g.user = None


def start_session(user):
    session.clear()
    session["user_id"] = user["user_id"]
    session["username"] = user["username"]


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if g.user:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        error = None
        if not username or not email or not password:
            error = "All fields are required."
        elif len(username) > 50:
            error = "Username must be 50 characters or fewer."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm:
            error = "Passwords do not match."
        if error is None:
            try:
                with transaction():
                    user = query(
                        """
                        INSERT INTO listener (username, password_hash, email)
                        VALUES (%s, crypt(%s, gen_salt('bf')), %s)
                        RETURNING user_id, username
                        """,
                        (username, password, email),
                        one=True,
                    )
                    query("INSERT INTO song_library (user_id) VALUES (%s)", (user["user_id"],))
            except errors.UniqueViolation as e:
                if e.diag.constraint_name == "listener_username_key":
                    error = "That username is already taken."
                else:
                    error = "That email is already registered."
            except errors.CheckViolation:
                error = "Please enter a valid email address."
            else:
                start_session(user)
                flash(f"Welcome to MuseLib, {user['username']}!", "success")
                return redirect(url_for("main.index"))
        flash(error, "error")
    return render_template("auth/signup.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = query(
            """
            SELECT user_id, username
            FROM listener
            WHERE username = %s AND password_hash = crypt(%s, password_hash)
            """,
            (username, password),
            one=True,
        )
        if user is None:
            flash("Incorrect username or password.", "error")
        else:
            start_session(user)
            return redirect(url_for("main.index"))
    return render_template("auth/login.html")


@bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
