from flask import Flask, jsonify, Response
from rediscluster import RedisCluster
import json
import random
import time
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, Counter, Gauge, Histogram

app = Flask(__name__)
metrics = PrometheusMetrics(app, labels={
    'service': 'activity-consumer',
    'application': 'flask-microservice',
    'environment': 'production'
})

# Metrics with Labels
REQUEST_COUNT = Counter(
    'request_count', 
    'App Request Count', 
    ['service', 'application', 'environment']
)
REQUEST_LATENCY = Histogram(
    'request_latency', 
    'Request latency', 
    ['service', 'application', 'environment']
)
IN_PROGRESS = Gauge(
    'in_progress', 
    'Number of requests in progress', 
    ['service', 'application', 'environment']
)

# Metric Labels
LABELS = {
    'service': 'activity-consumer',
    'application': 'flask-microservice',
    'environment': 'production'
}

# Redis Cluster Configuration
startup_nodes = [
    {"host": "redis-node1", "port": 6379},
    {"host": "redis-node2", "port": 6379},
    {"host": "redis-node3", "port": 6379}
]

# Connect to the Redis cluster
r = RedisCluster(startup_nodes=startup_nodes, 
                 decode_responses=True,
                 skip_full_coverage_check=True
)

# Define the Redis list name where activity logs are stored
ACTIVITY_LOG_LIST = "{activity_logs}"

# Simulate random failure (e.g., 20% failure rate)
def random_failure():
    if random.random() < 0.2:  # 20% chance to simulate a failure
        return True
    return False

@app.route('/activity_logs', methods=['GET'])
def get_activity_logs():
    # Increment request count
    REQUEST_COUNT.labels(**LABELS).inc()
    
    # Increment in-progress gauge
    IN_PROGRESS.labels(**LABELS).inc()

    try:
        # Measure request latency
        with REQUEST_LATENCY.labels(**LABELS).time():
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
            activity_logs = [json.loads(log if isinstance(log, str) else log.decode('utf-8')) for log in logs]
            return jsonify(activity_logs), 200

    finally:
        # Decrement in-progress gauge
        IN_PROGRESS.labels(**LABELS).dec()
    
@app.route('/health', methods=['GET'])
def health():
    try:
        # Simple ping to check Redis connectivity
        r.ping()
        return jsonify({
            "status": "OK", 
            "service": "activity-consumer",
            "environment": "production"
        }), 200
    except Exception as e:
        app.logger.error(f"Redis health check failed: {str(e)}")
        return jsonify({
            "status": "Error", 
            "message": "Redis cluster is not available"
        }), 503

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)