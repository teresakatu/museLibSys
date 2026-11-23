from flask import Blueprint, render_template

from routes.auth import login_required

bp = Blueprint("account", __name__)


@bp.route("/account")
@login_required
def index():
    return render_template("placeholder.html", title="Account")
