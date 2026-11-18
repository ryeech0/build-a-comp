# IMPORTS ==========
from flask import *
from flask_socketio import SocketIO
import requests
import dpp, scrape


# CONFIGS ==========
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, max_http_buffer_size=10485760)


# ROUTES ==========
@app.route("/")
def main():
    return render_template("index.html")