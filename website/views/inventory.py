import flask
from flask import Blueprint
from markupsafe import escape
from queries import *
from logging_config import logger

inventory_bp = Blueprint('inventory', __name__, url_prefix='/user')

@inventory_bp.route('/<name>')
async def index(name):
    query = """
            SELECT * FROM users
            WHERE username = %s;
            """
    user = await fetch_dict(query, params=(name,))
    logger.info(user)
    if user is None:
        flask.abort(404)
    return f"Hello, {escape(name)}"
