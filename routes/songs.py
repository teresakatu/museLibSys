from flask import Blueprint, g, render_template, request

from db import query
from routes.auth import login_required

bp = Blueprint("songs", __name__)

SORTS = {
    "title": ("Title (A–Z)", "LOWER(s.title)"),
    "artist": ("Artist (A–Z)", "LOWER(MIN(a.name)), LOWER(s.title)"),
    "newest": ("Newest first", "s.release_date DESC NULLS LAST, LOWER(s.title)"),
    "oldest": ("Oldest first", "s.release_date ASC NULLS LAST, LOWER(s.title)"),
}


def like_pattern(text):
    escaped = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


@bp.route("/songs")
@login_required
def browse():
    q = request.args.get("q", "").strip()
    genre = request.args.get("genre", "")
    sort = request.args.get("sort", "title")
    if sort not in SORTS:
        sort = "title"

    genres = [row["genre"] for row in query(
        "SELECT DISTINCT genre FROM song WHERE genre IS NOT NULL ORDER BY genre"
    )]
    if genre not in genres:
        genre = ""

    songs = query(
        f"""
        SELECT s.song_id,
               s.title,
               s.genre,
               s.release_date,
               TO_CHAR(MAKE_INTERVAL(secs => s.duration), 'MI:SS')       AS length,
               STRING_AGG(DISTINCT a.name, ', ' ORDER BY a.name)          AS artists,
               COALESCE(STRING_AGG(DISTINCT al.title, ', ' ORDER BY al.title),
                        '(single)')                                       AS album,
               BOOL_OR(ls.song_id IS NOT NULL)                            AS saved
        FROM song s
        JOIN song_artist sa       ON sa.song_id = s.song_id
        JOIN artist a             ON a.artist_id = sa.artist_id
        LEFT JOIN album_song als  ON als.song_id = s.song_id
        LEFT JOIN album al        ON al.album_id = als.album_id
        LEFT JOIN library_song ls ON ls.song_id = s.song_id
                                 AND ls.song_library_id = (SELECT song_library_id
                                                           FROM song_library
                                                           WHERE user_id = %(user_id)s)
        WHERE (%(genre)s = '' OR s.genre = %(genre)s)
        GROUP BY s.song_id
        HAVING %(q)s = ''
            OR s.title ILIKE %(pattern)s
            OR BOOL_OR(a.name ILIKE %(pattern)s)
            OR BOOL_OR(al.title ILIKE %(pattern)s)
        ORDER BY {SORTS[sort][1]}
        """,
        {"user_id": g.user["user_id"], "genre": genre, "q": q, "pattern": like_pattern(q)},
    )

    playlists = query(
        "SELECT playlist_id, name FROM playlist WHERE user_id = %s ORDER BY LOWER(name)",
        (g.user["user_id"],),
    )

    return render_template(
        "songs/browse.html",
        songs=songs,
        genres=genres,
        playlists=playlists,
        sorts=SORTS,
        q=q,
        genre=genre,
        sort=sort,
    )


@bp.route("/songs/new")
@login_required
def new():
    return render_template("placeholder.html", title="Add Song")
