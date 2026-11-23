from flask import Blueprint, abort, flash, g, render_template, request
from psycopg import errors

from db import query
from routes.auth import login_required
from routes.helpers import redirect_back

bp = Blueprint("playlists", __name__)


@bp.route("/playlists")
@login_required
def index():
    return render_template("placeholder.html", title="My Playlists")


@bp.route("/playlists/add-song", methods=("POST",))
@login_required
def add_song():
    playlist_id = request.form.get("playlist_id", type=int)
    song_id = request.form.get("song_id", type=int)
    playlist = query(
        "SELECT playlist_id, name FROM playlist WHERE playlist_id = %s AND user_id = %s",
        (playlist_id, g.user["user_id"]),
        one=True,
    )
    song = query("SELECT song_id, title FROM song WHERE song_id = %s", (song_id,), one=True)
    if playlist is None or song is None:
        abort(404)
    try:
        query(
            """
            INSERT INTO playlist_song (playlist_id, song_id, position)
            SELECT %(playlist_id)s,
                   %(song_id)s,
                   COALESCE((SELECT MAX(position) FROM playlist_song
                             WHERE playlist_id = %(playlist_id)s), 0) + 1
            """,
            {"playlist_id": playlist_id, "song_id": song_id},
        )
    except errors.UniqueViolation:
        flash(f"“{song['title']}” is already in {playlist['name']}.", "error")
    else:
        flash(f"Added “{song['title']}” to {playlist['name']}.", "success")
    return redirect_back("playlists.index", f"song-{song_id}")
