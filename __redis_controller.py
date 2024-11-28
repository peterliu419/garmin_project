import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Define the Redis list name where activity logs are stored
ACTIVITY_LOG_LIST = "activity_logs"

# Function to check the data in Redis
def check_redis_data():
    # Get the number of items in the Redis list
    length = r.llen(ACTIVITY_LOG_LIST)
    print(f"Number of activity logs in Redis: {length}")

    if length > 0:
        # Retrieve all items in the list
        activity_logs = r.lrange(ACTIVITY_LOG_LIST, 0, -1)
        print(f"Found {len(activity_logs)} activity logs in Redis:")
        
        # Loop through and print each log (decoded from JSON)
        for idx, log_data in enumerate(activity_logs, 1):
            activity_log = json.loads(log_data)
            print(f"\nLog {idx}:")
            print(json.dumps(activity_log, indent=4))
    else:
        print("No activity logs found in Redis.")

# Optional: Delete all logs from Redis (use with caution)
def clear_redis_data():
    confirmation = input("Are you sure you want to delete all activity logs from Redis? (y/n): ")
    if confirmation.lower() == 'y':
        r.delete(ACTIVITY_LOG_LIST)
        print("All activity logs deleted from Redis.")
    else:
        print("No data was deleted.")

# Main function
if __name__ == '__main__':
    check_redis_data()

    # Optionally, you can clear the Redis data if desired
    #clear_redis_data()

