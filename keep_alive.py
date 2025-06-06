from flask import Flask
import socket
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
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
