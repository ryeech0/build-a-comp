# IMPORTS ==========
from flask import *
from flask_socketio import SocketIO
import requests
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
@socketio.on("agent_selected")
def update_comp_data():
    pass

@socketio.on("map_selected")
def update_stat_data(map: str):
    # print(map)
    res_dict = {}
    agent_pickrates = dpp.get_all_agent_pickrates(map)
    agent_winrates = dpp.calculate_all_agents_winrates(map)
    agents_list = dpp.get_agents_list()
    for agent in agents_list:
        res_dict[agent] = {
            "pickrate": agent_pickrates[agent], 
            "winrate": agent_winrates[agent]
        }
    # print(res_dict)
    socketio.emit("map_data_sent", res_dict)


if __name__ == "__main__":
    socketio.run(app, debug=True)