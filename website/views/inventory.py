from zoneinfo import ZoneInfo
import flask
from flask import Blueprint, render_template
from markupsafe import escape
from queries import *

from logging_config import logger

inventory_bp = Blueprint('inventory', __name__, url_prefix='/user')

@inventory_bp.route('/<name>')
def index(name):
    name = escape(name)
    query = """
            SELECT * FROM users
            WHERE username = %s;
            """
    user = fetch_dict(query, params=(name,))
    if user is None:
        flask.abort(404)
    # Have user now
    
    query = """
            WITH u_gifs (user_id, gif_id, obtain_date) AS (
                SELECT user_gifs.user_id, user_gifs.gif_id, user_gifs.obtain_date 
                FROM user_gifs
                WHERE user_gifs.user_id = %s
            )
            SELECT gifs.url, gifs.tier, u_gifs.obtain_date, gifs.id
            FROM gifs
            INNER JOIN u_gifs ON u_gifs.gif_id = gifs.id
            ORDER BY
                CASE gifs.tier
                    WHEN 'S' THEN 1
                    WHEN 'A' THEN 2
                    WHEN 'B' THEN 3
                    WHEN 'C' THEN 4
            END,
            u_gifs.obtain_date DESC;
            """
    user_gifs_sorted = fetch_dict_all(query, params=(user['user_id'],))

    est = ZoneInfo("US/Eastern")
    for idx, gif in enumerate(user_gifs_sorted):
        date_time = gif['obtain_date'].astimezone(est)
        user_gifs_sorted[idx]['obtain_date'] = date_time.strftime('%B %-d, %Y at %-I:%M %p')

    query = """
            with f_gifs (id, favorited_at) AS (
                SELECT gif_id, favorited_at
                FROM user_favorites
                WHERE user_id = %s
                ORDER BY favorited_at
            )
            SELECT f_gifs.id, gifs.tier, gifs.url, f_gifs.favorited_at
            FROM f_gifs
            INNER JOIN gifs ON f_gifs.id = gifs.id
            ORDER BY f_gifs.favorited_at;
            """

    favorite_gifs = fetch_dict_all(query, params=(user['user_id'],))

    for idx, gif in enumerate(favorite_gifs):
        date_time = gif['favorited_at'].astimezone(est)
        favorite_gifs[idx]['favorited_at'] = date_time.strftime('%B %-d, %Y at %-I:%M %p')

    context = {
        "username": name,
        "user_gifs": user_gifs_sorted,
        "fav_gifs": favorite_gifs,
    }
    return render_template("inventory.html", **context)
