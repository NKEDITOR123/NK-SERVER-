from flask import Flask, request, jsonify
from tasks import start_task, stop_task
import json

app = Flask(__name__)
sessions = {}

@app.route('/pair', methods=['POST'])
def pair():
    number = request.json['number']
    # Baileys pairing logic here
    sessions[number] = {"status": "paired"}
    return jsonify({"status": "paired", "number": number})

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    task_id = start_task(data)
    return jsonify({"task_id": task_id})

@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.json['task_id']
    stop_task(task_id)
    return jsonify({"status": "stopped", "task_id": task_id})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "active_sessions": len(sessions),
        "active_tasks": len(open_tasks)
    })

if __name__ == '__main__':
    app.run(debug=True)
