# IMPORTS ==========
from flask import *
from flask_socketio import SocketIO
import requests
import dotenv
import dpp


# CONFIGS ==========
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, max_http_buffer_size=10485760)


# ROUTES ==========
@app.route("/")
def init_landing():
    return render_template("index.html")

@app.route("/build")
def init_build():
    agents_dict = dpp.read_agents_data_from_json()
    return render_template("build.html", agents_dict=agents_dict)


# PAGE UPDATES ==========