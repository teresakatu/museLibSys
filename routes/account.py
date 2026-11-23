from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from psycopg import errors

from db import query
from routes.auth import login_required

bp = Blueprint("account", __name__)


def listener_summary(user_id):
    return query(
        """
        SELECT l.username,
               l.email,
               l.created_date,
               (SELECT COUNT(*)
                FROM library_song ls
                JOIN song_library sl ON sl.song_library_id = ls.song_library_id
                WHERE sl.user_id = l.user_id)                     AS saved_count,
               (SELECT COUNT(*)
                FROM playlist p
                WHERE p.user_id = l.user_id)                      AS playlist_count
        FROM listener l
        WHERE l.user_id = %s
        """,
        (user_id,),
        one=True,
    )


@bp.route("/account")
@login_required
def index():
    summary = listener_summary(g.user["user_id"])
    if summary is None:
        session.clear()
        return redirect(url_for("auth.login"))
    return render_template("account/index.html", summary=summary)


@bp.route("/account/email", methods=("POST",))
@login_required
def change_email():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("current_password", "")
    error = None
    if not email or not password:
        error = "Enter a new email and your current password."
    elif len(email) > 255:
        error = "Email must be 255 characters or fewer."
    else:
        try:
            updated = query(
                """
                UPDATE listener
                SET    email = %s
                WHERE  user_id = %s
                  AND  password_hash = crypt(%s, password_hash)
                RETURNING email
                """,
                (email, g.user["user_id"], password),
                one=True,
            )
        except errors.UniqueViolation:
            error = "That email is already registered."
        except errors.CheckViolation:
            error = "Please enter a valid email address."
        else:
            if updated is None:
                error = "Current password is incorrect."
            else:
                flash(f"Email updated to {updated['email']}.", "success")
    if error:
        flash(error, "error")
    return redirect(url_for("account.index"))


@bp.route("/account/password", methods=("POST",))
@login_required
def change_password():
    current = request.form.get("current_password", "")
    new = request.form.get("new_password", "")
    confirm = request.form.get("confirm", "")
    error = None
    if not current or not new:
        error = "Enter your current password and a new password."
    elif len(new) < 8:
        error = "New password must be at least 8 characters."
    elif new != confirm:
        error = "New passwords do not match."
    else:
        updated = query(
            """
            UPDATE listener
            SET    password_hash = crypt(%s, gen_salt('bf'))
            WHERE  user_id = %s
              AND  password_hash = crypt(%s, password_hash)
            RETURNING user_id
            """,
            (new, g.user["user_id"], current),
            one=True,
        )
        if updated is None:
            error = "Current password is incorrect."
        else:
            flash("Password changed.", "success")
    if error:
        flash(error, "error")
    return redirect(url_for("account.index"))


@bp.route("/account/delete", methods=("POST",))
@login_required
def delete():
    password = request.form.get("current_password", "")
    deleted = query(
        """
        DELETE FROM listener
        WHERE user_id = %s
          AND password_hash = crypt(%s, password_hash)
        RETURNING username
        """,
        (g.user["user_id"], password),
        one=True,
    )
    if deleted is None:
        flash("Current password is incorrect. Your account was not deleted.", "error")
        return redirect(url_for("account.index"))
    session.clear()
    flash(f"Account “{deleted['username']}” and all of its data were deleted.", "success")
    return redirect(url_for("auth.signup"))
