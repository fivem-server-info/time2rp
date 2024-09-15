from flask import Flask, jsonify, render_template
# from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import requests
import time
import json
from datetime import datetime

app = Flask(__name__)

sched = APScheduler()
sched.api_enabled = True
sched.init_app(app)

SERVER_URL = "https://servers-frontend.fivem.net/api/servers/single/k8px4v"
player_data = {}
previous_players = []
logs = []

@app.template_filter('format_time')
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def fetch_server_data():
    headers = {
        "Accept": '*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(SERVER_URL, headers=headers)
        if response.status_code == 200:
            return response.json(), "online"
        elif response.status_code == 404:
            return None, "offline"
        else:
            print(f"Error: {response.status_code}")
            return None, response.status_code
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, e

def update_player_data():
    global player_data, previous_players, logs
    server_info, server_status = fetch_server_data()

    if server_info and server_status == "online":
        current_players = server_info['Data']['players']
        current_ids = [player["id"] for player in current_players]
    elif server_status == "offline":
        current_players = {}
        current_ids = []
    else:
        return None

    # Check for players who have left
    players_left = [pid for pid in list(player_data.keys()) if pid not in current_ids]
    for pid in players_left:
        player_info = player_data.pop(pid, None)
        if player_info:
            join_time = player_info.get("join_time")
            time_played_seconds = time.time() - join_time

            # Convert seconds into hours, minutes, and seconds
            hours, remainder = divmod(time_played_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Format the time played
            time_played_formatted = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

            readable_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S %d/%m/%Y')
            leave_log = [
                readable_time,
                pid,
                f"<span style='color: red;'><b>{player_info.get('name')}</b> left the server | Time played: {time_played_formatted}</span>"
                ]
            logs.append(leave_log)

    # Check for new players (joins)
    new_players = [player for player in current_players if player['id'] not in previous_players]
    for player in new_players:
        player_id = player['id']
        if player_id not in list(player_data.keys()):
            steam_dec_id = None
            discord_id = None
            for identifier in player["identifiers"]:
                if identifier.startswith("steam:"):
                    steam_dec_id = int(identifier.split(":")[1], 16)
                if identifier.startswith("discord:"):
                    discord_id = identifier.split(":")[1]
            player_data[player_id] = {
                'id': player_id,
                'name': player['name'],
                'join_time': time.time(),
                'discord': discord_id,
                'steam': steam_dec_id,
                'ping': player['ping']
            }
            readable_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S %d/%m/%Y')
            join_log = [
                readable_time,
                player['id'],
                f"<span style='color: green;'><b>{player['name']}</b> joined the server | {min(len(player_data), 150)}/150</span>"
                ]
            logs.append(join_log)

    previous_players = current_ids

@app.route('/players')
def players():
    server_info, server_status = fetch_server_data()
    avatar = "https://forum.cfx.re/user_avatar/forum.cfx.re/time2rp/128/4515793_2.png"
    if server_info:
        # current_players = server_info['Data']['players']
        # host_name = server_info['Data']['hostname']
        # avatar = server_info['Data']['ownerAvatar']
        current_time = time.time()
        return render_template("index.html", server_status=server_status, avatar=avatar, current_time=current_time, player_count=len(player_data), player_data=player_data)
    else:
        return render_template("index.html", server_status=server_status, avatar=avatar)
    
@app.route('/logs')
def logs_func():
    server_info, server_status = fetch_server_data()
    avatar = "https://forum.cfx.re/user_avatar/forum.cfx.re/time2rp/128/4515793_2.png"
    if server_info:
        return render_template("logs.html", server_status=server_status, avatar=avatar, logs=logs, player_count=len(player_data))
    else:
        return render_template("logs.html", server_status=server_status, avatar=avatar)

if __name__ == '__main__':
    sched.add_job(id="update_player_data", func=update_player_data, trigger="interval", seconds=10, max_instances=1)
    sched.start()
    app.run(debug=True, use_reloader=False)
