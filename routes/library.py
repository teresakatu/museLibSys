from flask import Blueprint, abort, flash, g, render_template

from db import query
from routes.auth import login_required
from routes.helpers import redirect_back

bp = Blueprint("library", __name__)


@bp.route("/library")
@login_required
def index():
    return render_template("placeholder.html", title="My Library")


def song_title(song_id):
    song = query("SELECT title FROM song WHERE song_id = %s", (song_id,), one=True)
    if song is None:
        abort(404)
    return song["title"]


@bp.route("/library/<int:song_id>/save", methods=("POST",))
@login_required
def save(song_id):
    title = song_title(song_id)
    query(
        """
        INSERT INTO library_song (song_library_id, song_id)
        SELECT song_library_id, %s
        FROM song_library
        WHERE user_id = %s
        ON CONFLICT (song_library_id, song_id) DO NOTHING
        """,
        (song_id, g.user["user_id"]),
    )
    flash(f"Saved “{title}” to your library.", "success")
    return redirect_back("library.index", f"song-{song_id}")


@bp.route("/library/<int:song_id>/remove", methods=("POST",))
@login_required
def remove(song_id):
    title = song_title(song_id)
    query(
        """
        DELETE FROM library_song
        WHERE song_library_id = (SELECT song_library_id
                                 FROM song_library
                                 WHERE user_id = %s)
          AND song_id = %s
        """,
        (g.user["user_id"], song_id),
    )
    flash(f"Removed “{title}” from your library.", "success")
    return redirect_back("library.index", f"song-{song_id}")
