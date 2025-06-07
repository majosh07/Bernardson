from flask import Flask
import socket
from threading import Thread
from flask import Flask
import asyncio
import logging

app = Flask(__name__)
db = None

@app.route("/ping-db")
def ping_db():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def run_check():
        try:
            if db is None or db.pool is None:
                return "DB not initliazed", 500
            async with db.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1;")
            return "OK"
        except Exception as e:
            return f"DB error: {e}"

    return loop.run_until_complete(run_check())

class FilterPingDB(logging.Filter):
    def filter(self, record):
        return '/ping-db' not in record.getMessage()
log = logging.getLogger('werkzeug')
log.addFilter(FilterPingDB())

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive(database):
    global db
    db = database
    t = Thread(target=run)
    t.start()


def get_ipv4(hostname):
    try:
        results = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
        if not results:
            raise RuntimeError(f"No IPv4 address found for {hostname}")
        return results[0][4][0]  # This gives the IPv4 address string
    except socket.gaierror as e:
        raise RuntimeError(f"DNS resolution failed for {hostname}: {e}")
