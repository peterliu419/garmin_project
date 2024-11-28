import requests
import random
import time

# The URL of the consumer Flask API
CONSUMER_API_URL = "http://127.0.0.1:5001/activity_logs"

# Function to call the consumer API and handle the response
def call_consumer_api():
    try:
        response = requests.get(CONSUMER_API_URL)
        
        # Simulate a random delay before each request to mimic real-world scenarios
        time.sleep(random.uniform(0.5, 2))

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

# Simulate calling the API multiple times
def simulate_calls():
    for _ in range(10):  # Make 10 API calls
        call_consumer_api()

if __name__ == '__main__':
    simulate_calls()
