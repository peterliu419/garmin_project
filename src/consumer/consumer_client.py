from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
import time

# The URL of the consumer Flask API
CONSUMER_API_URL = "http://consumer_app:5002/activity_logs"

# Function to simulate random failure (20% chance of failure)
def random_failure():
    return random.random() < 0.2  # 20% chance of failure

# Function to call the consumer API and handle the response
def call_consumer_api():
    # Simulate a random delay before each request to mimic real-world scenarios
    time.sleep(random.uniform(0.5, 2))  # Random delay between 0.5 to 2 seconds

    # Simulate random failure
    if random_failure():
        print("Error: Random failure occurred in the consumer API.")
        return

    try:
        response = requests.get(CONSUMER_API_URL)

        if response.status_code == 200:
            print("Successfully retrieved activity logs:")
            print(response.json())  # Print the activity logs from the response
        elif response.status_code == 404:
            print("No activity logs found.")
        elif response.status_code == 500:
            print("Error: Random failure occurred in the consumer API.")
        else:
            print(f"Unexpected error occurred: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request to consumer API: {e}")

# Create and start the scheduler for periodic API calls
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Add job with a unique id to call the consumer API every 15 seconds
    scheduler.add_job(func=call_consumer_api, trigger='interval', seconds=15, id="call_consumer_api_job")

    # Start the scheduler
    scheduler.start()

    # Keep the script running to allow the scheduler to run
    try:
        while True:
            time.sleep(1)  # To keep the program running and allow the scheduler to run
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

# Start the scheduled activity generator
if __name__ == '__main__':
    start_scheduler()
