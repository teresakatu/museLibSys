from flask import Blueprint, render_template

from routes.auth import login_required

bp = Blueprint("library", __name__)


@bp.route("/library")
@login_required
def index():
    return render_template("placeholder.html", title="My Library")
