from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Define the Redis list name where activity logs will be stored
ACTIVITY_LOG_LIST = "activity_logs"

@app.route('/log_activity', methods=['POST'])
def log_activity():
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

if __name__ == '__main__':
    app.run(debug=True)
