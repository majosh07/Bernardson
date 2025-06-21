from flask import Flask
from threading import Thread
import logging

from website.views.ping_db import ping_bp
from website.views.inventory import inventory_bp

app = Flask(__name__)

app.register_blueprint(ping_bp)
app.register_blueprint(inventory_bp)


class FilterPingDB(logging.Filter):
    def filter(self, record):
        return '/ping-db' not in record.getMessage()
log = logging.getLogger('werkzeug')
log.addFilter(FilterPingDB())

def flask_run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def website_run():
    t = Thread(target=flask_run)
    t.daemon = True
    t.start()


