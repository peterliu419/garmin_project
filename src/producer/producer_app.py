from flask import Flask, request, jsonify, Response
from rediscluster import RedisCluster
import json
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, Counter, Gauge, Histogram
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metrics (unchanged)
REQUEST_COUNT = Counter('request_count', 'App Request Count')
REQUEST_LATENCY = Histogram('request_latency', 'Request latency')
IN_PROGRESS = Gauge('in_progress', 'Number of requests in progress')

# Redis Cluster Configuration
startup_nodes = [
    {"host": "redis-node1", "port": 6379},
    {"host": "redis-node2", "port": 6379},
    {"host": "redis-node3", "port": 6379}
]

def create_redis_connection(max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            r = RedisCluster(
                startup_nodes=startup_nodes, 
                decode_responses=True,
                skip_full_coverage_check=False,
                # Add timeout and connection parameters
                socket_timeout=5,
                socket_connect_timeout=5,
                max_connections=20
            )
            # Perform a simple ping to verify connection
            r.ping()
            return r
        except Exception as e:
            logger.warning(f"Redis connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

# Initialize Redis connection on startup
try:
    r = create_redis_connection()
except Exception as e:
    logger.error(f"Could not establish Redis connection: {e}")
    r = None

# Define the Redis list name where activity logs will be stored
ACTIVITY_LOG_LIST = "{activity_logs}"

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

        # Retry mechanism for Redis operations
        max_retries = 3
        for attempt in range(max_retries):
            try:
                r.rpush(ACTIVITY_LOG_LIST, json.dumps(activity_log))
                break
            except Exception as e:
                logger.warning(f"Redis push attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return jsonify({"error": "Failed to log activity"}), 500

        return jsonify({"message": "Activity logged successfully"}), 200

@app.route('/health', methods=['GET'])
def health():
    try:
        # Simple ping to check Redis connectivity
        r.ping()
        return "OK", 200
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Redis health check failed: {str(e)}")
        return "Redis cluster is not available", 503

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5001)
