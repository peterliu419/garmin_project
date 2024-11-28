from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
from datetime import datetime
import time

# Flask API endpoint
API_URL = "http://127.0.0.1:5000/log_activity"
#"http://localhost:5000/log_activity"


# Function to generate random activity data
def generate_random_activity():
    activity_types = ["running", "cycling", "swimming", "hiking"]
    activity_statuses = ["completed", "paused", "in_progress"]

    # Randomly generate data for the activity log
    activity_log = {
        "user_id": random.randint(1, 10),  # Random user ID (simulate 10 users)
        "activity_type": random.choice(activity_types),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration": random.randint(600, 3600),  # Random duration between 10 min to 1 hour
        "distance": round(random.uniform(1.0, 20.0), 2),  # Random distance (1 to 20 km)
        "heart_rate": random.randint(120, 180),  # Random heart rate
        "calories_burned": random.randint(200, 800),  # Random calories burned
        "location": {
            "latitude": round(random.uniform(37.0, 38.0), 4),  # Random latitude (37.0 to 38.0)
            "longitude": round(random.uniform(-123.0, -122.0), 4)  # Random longitude (-123.0 to -122.0)
        },
        "device_id": f"watch_{random.randint(1, 5)}",  # Random device ID (simulate 5 devices)
        "activity_status": random.choice(activity_statuses)
    }

    return activity_log

# Function to send the random activity log to the Flask API
def send_random_activity():
    activity_log = generate_random_activity()
    response = requests.post(API_URL, json=activity_log)
    
    if response.status_code == 200:
        print("Successfully logged activity:", activity_log)
    else:
        print("Failed to log activity:", response.status_code)

# Create and start the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Add job with a unique id
    scheduler.add_job(func=send_random_activity, trigger='interval', seconds=10, id="send_random_data_job")

    # Start the scheduler
    scheduler.start()

    # Keep the script running
    try:
        while True:
            time.sleep(1)  # To keep the program running and allow the scheduler to run
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

# Start the scheduled activity generator
if __name__ == '__main__':
    start_scheduler()
