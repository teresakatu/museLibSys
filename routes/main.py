from flask import Blueprint, g, redirect, render_template, session, url_for

from db import query
from routes.account import listener_summary
from routes.auth import login_required

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    user_id = g.user["user_id"]
    summary = listener_summary(user_id)
    if summary is None:
        session.clear()
        return redirect(url_for("auth.login"))

    playlists = query(
        """
        SELECT p.playlist_id,
               p.name,
               COUNT(ps.song_id) AS song_count
        FROM playlist p
        LEFT JOIN playlist_song ps ON ps.playlist_id = p.playlist_id
        WHERE p.user_id = %s
        GROUP BY p.playlist_id
        ORDER BY p.created_date DESC
        LIMIT 4
        """,
        (user_id,),
    )

    recent = query(
        """
        SELECT s.song_id,
               s.title,
               STRING_AGG(a.name, ', ' ORDER BY a.name) AS artists,
               ls.saved_date
        FROM library_song ls
        JOIN song_library sl ON sl.song_library_id = ls.song_library_id
        JOIN song s          ON s.song_id = ls.song_id
        JOIN song_artist sa  ON sa.song_id = s.song_id
        JOIN artist a        ON a.artist_id = sa.artist_id
        WHERE sl.user_id = %s
        GROUP BY s.song_id, ls.saved_date
        ORDER BY ls.saved_date DESC
        LIMIT 5
        """,
        (user_id,),
    )

    trending = query(
        """
        SELECT s.title,
               STRING_AGG(DISTINCT a.name, ', ')        AS artists,
               COUNT(DISTINCT ls.song_library_id)       AS times_saved,
               COUNT(DISTINCT ps.playlist_id)           AS on_playlists
        FROM song s
        JOIN song_artist sa        ON sa.song_id = s.song_id
        JOIN artist a              ON a.artist_id = sa.artist_id
        JOIN library_song ls       ON ls.song_id = s.song_id
        LEFT JOIN playlist_song ps ON ps.song_id = s.song_id
        GROUP BY s.song_id, s.title
        HAVING COUNT(DISTINCT ls.song_library_id) >= 2
        ORDER BY times_saved DESC, on_playlists DESC, s.title
        LIMIT 5
        """
    )

    return render_template(
        "main/index.html",
        summary=summary,
        playlists=playlists,
        recent=recent,
        trending=trending,
    )
