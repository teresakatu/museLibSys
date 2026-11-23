from flask import Blueprint, render_template

from routes.auth import login_required

bp = Blueprint("songs", __name__)


@bp.route("/songs")
@login_required
def browse():
    return render_template("placeholder.html", title="Browse & Search")


@bp.route("/songs/new")
@login_required
def new():
    return render_template("placeholder.html", title="Add Song")
