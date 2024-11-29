from flask import Flask, request, jsonify,Response
from rediscluster import RedisCluster
import json
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, Counter, Gauge, Histogram

app = Flask(__name__)
# metrics = PrometheusMetrics(app)
# Define metrics
REQUEST_COUNT = Counter('request_count', 'App Request Count')
REQUEST_LATENCY = Histogram('request_latency', 'Request latency')
IN_PROGRESS = Gauge('in_progress', 'Number of requests in progress')

# Redis Cluster Configuration
startup_nodes = [
    {"host": "redis-node1", "port": 6379},
    {"host": "redis-node2", "port": 6380},
    {"host": "redis-node3", "port": 6381}
]

# Connect to the Redis cluster
r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Define the Redis list name where activity logs will be stored
ACTIVITY_LOG_LIST = "activity_logs"

@app.route('/log_activity', methods=['POST'])
def log_activity():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        # Get activity data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ["user_id", "activity_type", "timestamp", "duration", "distance", "heart_rate", "calories_burned", "location", "device_id", "activity_status"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure timestamp is in the correct format
        try:
            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return jsonify({"error": "Invalid timestamp format, should be YYYY-MM-DDTHH:MM:SSZ"}), 400

        # Prepare the activity log to be stored in Redis
        activity_log = {
            "user_id": data["user_id"],
            "activity_type": data["activity_type"],
            "timestamp": timestamp.isoformat(),
            "duration": data["duration"],
            "distance": data["distance"],
            "heart_rate": data["heart_rate"],
            "calories_burned": data["calories_burned"],
            "location": data["location"],
            "device_id": data["device_id"],
            "activity_status": data["activity_status"]
        }

        # Push the activity log to Redis (stored as JSON string)
        r.rpush(ACTIVITY_LOG_LIST, json.dumps(activity_log))

        return jsonify({"message": "Activity logged successfully"}), 200
    
    IN_PROGRESS.dec()

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5001)
