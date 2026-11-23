from flask import Blueprint, render_template

from routes.auth import login_required

bp = Blueprint("playlists", __name__)


@bp.route("/playlists")
@login_required
def index():
    return render_template("placeholder.html", title="My Playlists")
