import os

import psycopg
from flask import g
from psycopg.rows import dict_row


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(
            os.environ["DATABASE_URL"],
            autocommit=True,
            row_factory=dict_row,
            prepare_threshold=None,
        )
    return g.db


def close_db(exception=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def query(sql, params=None, one=False):
    with get_db().cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall() if cur.description else []
    if one:
        return rows[0] if rows else None
    return rows


def transaction():
    return get_db().transaction()


def init_app(app):
    app.teardown_appcontext(close_db)
