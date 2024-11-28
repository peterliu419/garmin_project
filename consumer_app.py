from flask import Flask, jsonify
import redis
import json
import random
import time
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Connect to Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Define the Redis list name where activity logs are stored
ACTIVITY_LOG_LIST = "activity_logs"

# Simulate random failure (e.g., 20% failure rate)
def random_failure():
    if random.random() < 0.2:  # 20% chance to simulate a failure
        return True
    return False

@app.route('/activity_logs', methods=['GET'])
def get_activity_logs():
    # Introduce random delay (for simulation purposes)
    time.sleep(random.uniform(0.5, 2))  # Random delay between 0.5 and 2 seconds

    # Simulate random failure
    if random_failure():
        return jsonify({"error": "Random failure occurred"}), 500

    # Retrieve all activity logs from Redis
    logs = r.lrange(ACTIVITY_LOG_LIST, 0, -1)

    # If no logs are found, return a 404
    if not logs:
        return jsonify({"message": "No activity logs found"}), 404

    # Convert the logs from byte strings to JSON and return
    activity_logs = [json.loads(log.decode('utf-8')) for log in logs]
    return jsonify(activity_logs), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)