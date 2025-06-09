from flask import Flask
import socket
from threading import Thread
from flask import Flask
import asyncio
import logging
from pool import pool

app = Flask(__name__)


@app.route("/ping-db")
def ping_db():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def run_check():
        try:
            if pool is None:
                return "Pool not initialiazed", 500
            async with pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1;")
            return "OK"
        except Exception as e:
            return f"pool error: {e}"

    return loop.run_until_complete(run_check())

class FilterPingDB(logging.Filter):
    def filter(self, record):
        return '/ping-db' not in record.getMessage()
log = logging.getLogger('werkzeug')
log.addFilter(FilterPingDB())

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = Thread(target=run)
    t.start()


