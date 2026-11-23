from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from psycopg import errors

from db import query, transaction
from routes.auth import login_required
from routes.helpers import redirect_back

bp = Blueprint("playlists", __name__)


@bp.app_template_filter("total_length")
def total_length(seconds):
    minutes = round((seconds or 0) / 60)
    if minutes < 60:
        return f"{minutes} min"
    return f"{minutes // 60} hr {minutes % 60} min"


def get_own_playlist(playlist_id):
    playlist = query(
        """
        SELECT playlist_id, name, description, created_date
        FROM playlist
        WHERE playlist_id = %s AND user_id = %s
        """,
        (playlist_id, g.user["user_id"]),
        one=True,
    )
    if playlist is None:
        abort(404)
    return playlist


def read_playlist_form():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip() or None
    error = None
    if not name:
        error = "Playlist name is required."
    elif len(name) > 100:
        error = "Playlist name must be 100 characters or fewer."
    return name, description, error


@bp.route("/playlists")
@login_required
def index():
    playlists = query(
        """
        SELECT p.playlist_id,
               p.name,
               p.description,
               p.created_date,
               COUNT(ps.song_id)             AS song_count,
               COALESCE(SUM(s.duration), 0)  AS total_seconds
        FROM playlist p
        LEFT JOIN playlist_song ps ON ps.playlist_id = p.playlist_id
        LEFT JOIN song s           ON s.song_id = ps.song_id
        WHERE p.user_id = %s
        GROUP BY p.playlist_id
        ORDER BY p.created_date DESC
        """,
        (g.user["user_id"],),
    )
    return render_template("playlists/index.html", playlists=playlists)


@bp.route("/playlists", methods=("POST",))
@login_required
def create():
    name, description, error = read_playlist_form()
    if error is None:
        try:
            playlist = query(
                """
                INSERT INTO playlist (user_id, name, description)
                VALUES (%s, %s, %s)
                RETURNING playlist_id
                """,
                (g.user["user_id"], name, description),
                one=True,
            )
        except errors.UniqueViolation:
            error = f"You already have a playlist named “{name}”."
        else:
            flash(f"Created playlist “{name}”.", "success")
            return redirect(url_for("playlists.detail", playlist_id=playlist["playlist_id"]))
    flash(error, "error")
    return redirect(url_for("playlists.index"))


@bp.route("/playlists/<int:playlist_id>")
@login_required
def detail(playlist_id):
    playlist = get_own_playlist(playlist_id)
    songs = query(
        """
        SELECT ps.position,
               s.song_id,
               s.title,
               s.duration,
               TO_CHAR(MAKE_INTERVAL(secs => s.duration), 'MI:SS')       AS length,
               STRING_AGG(DISTINCT a.name, ', ' ORDER BY a.name)          AS artists,
               COALESCE(STRING_AGG(DISTINCT al.title, ', ' ORDER BY al.title),
                        '(single)')                                       AS album,
               ps.added_date
        FROM playlist_song ps
        JOIN song s              ON s.song_id = ps.song_id
        JOIN song_artist sa      ON sa.song_id = s.song_id
        JOIN artist a            ON a.artist_id = sa.artist_id
        LEFT JOIN album_song als ON als.song_id = s.song_id
        LEFT JOIN album al       ON al.album_id = als.album_id
        WHERE ps.playlist_id = %s
        GROUP BY ps.position, s.song_id, ps.added_date
        ORDER BY ps.position
        """,
        (playlist_id,),
    )
    total_seconds = sum(s["duration"] for s in songs)
    return render_template(
        "playlists/detail.html",
        playlist=playlist,
        songs=songs,
        total_seconds=total_seconds,
    )


@bp.route("/playlists/<int:playlist_id>/edit", methods=("POST",))
@login_required
def edit(playlist_id):
    get_own_playlist(playlist_id)
    name, description, error = read_playlist_form()
    if error is None:
        try:
            query(
                """
                UPDATE playlist
                SET    name = %s,
                       description = %s
                WHERE  playlist_id = %s
                  AND  user_id = %s
                """,
                (name, description, playlist_id, g.user["user_id"]),
            )
        except errors.UniqueViolation:
            error = f"You already have a playlist named “{name}”."
        else:
            flash("Playlist updated.", "success")
    if error:
        flash(error, "error")
    return redirect(url_for("playlists.detail", playlist_id=playlist_id))


@bp.route("/playlists/<int:playlist_id>/delete", methods=("POST",))
@login_required
def delete(playlist_id):
    playlist = get_own_playlist(playlist_id)
    query(
        "DELETE FROM playlist WHERE playlist_id = %s AND user_id = %s",
        (playlist_id, g.user["user_id"]),
    )
    flash(f"Deleted playlist “{playlist['name']}”.", "success")
    return redirect(url_for("playlists.index"))


@bp.route("/playlists/<int:playlist_id>/songs/<int:song_id>/remove", methods=("POST",))
@login_required
def remove_song(playlist_id, song_id):
    get_own_playlist(playlist_id)
    with transaction():
        removed = query(
            """
            DELETE FROM playlist_song
            WHERE playlist_id = %s AND song_id = %s
            RETURNING position,
                      (SELECT title FROM song WHERE song_id = playlist_song.song_id) AS title
            """,
            (playlist_id, song_id),
            one=True,
        )
        if removed is None:
            abort(404)
        query(
            """
            UPDATE playlist_song
            SET    position = position - 1
            WHERE  playlist_id = %s
              AND  position > %s
            """,
            (playlist_id, removed["position"]),
        )
    flash(f"Removed “{removed['title']}” from this playlist.", "success")
    return redirect(url_for("playlists.detail", playlist_id=playlist_id))


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
