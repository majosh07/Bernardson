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
    
    context = {
        "username": name,
        "user_gifs": user_gifs_sorted,
    }

    return render_template("inventory.html", **context)
