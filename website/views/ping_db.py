from flask import Blueprint
import asyncio
from pool import pool


ping_bp = Blueprint('ping-db', __name__, url_prefix='/')

@ping_bp.route("/ping-db")
def ping_db():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def run_check():
        try:
            if pool is None:
                return "Pool not initialized", 500
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
            return "OK"
        except Exception as e:
            return f"pool error: {e}"

    return loop.run_until_complete(run_check())

