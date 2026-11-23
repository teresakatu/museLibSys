from flask import Blueprint, render_template

from routes.auth import login_required

bp = Blueprint("trending", __name__)


@bp.route("/trending")
@login_required
def index():
    return render_template("placeholder.html", title="Trending")
