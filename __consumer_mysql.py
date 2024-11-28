import redis
import json
import mysql.connector
from time import sleep
from config import mysql_config

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# MySQL connection configuration
db_config = {
    "host": mysql_config["host"],
    "user": mysql_config["user"],
    "password": mysql_config["password"],
    "database": "activity_db"
}

# Connect to MySQL
def connect_mysql():
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

# Function to process and store activity data into MySQL
def process_and_store_activity_data(activity_log):
    try:
        # Connect to MySQL
        conn = connect_mysql()
        cursor = conn.cursor()

        # Prepare the SQL query to insert data into the 'activities' table
        query = """
        INSERT INTO activities (user_id, activity_type, timestamp, duration, distance, heart_rate, calories_burned, latitude, longitude, device_id, activity_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Extract values from the activity log
        values = (
            activity_log["user_id"],
            activity_log["activity_type"],
            activity_log["timestamp"],
            activity_log["duration"],
            activity_log["distance"],
            activity_log["heart_rate"],
            activity_log["calories_burned"],
            activity_log["location"]["latitude"],
            activity_log["location"]["longitude"],
            activity_log["device_id"],
            activity_log["activity_status"]
        )

        # Execute the query
        cursor.execute(query, values)
        conn.commit()

        print(f"Successfully stored activity log for user {activity_log['user_id']}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to consume data from Redis (blocking)
def consume_data_from_redis():
    print("Consumer started. Waiting for new data from Redis...")
    while True:
        # Fetch the first activity log from Redis (blocking operation)
        log_data = r.blpop("activity_logs", timeout=10)  # 'activity_logs' is the Redis list where activity logs are stored

        if log_data:
            # Convert the JSON string back into a Python dictionary
            activity_log = json.loads(log_data[1])  # log_data is a tuple (list_name, value), so we access [1] for the value
            process_and_store_activity_data(activity_log)
        
        # Sleep for a while before checking again (optional)
        sleep(1)  # Delay is optional, but can help reduce constant polling

if __name__ == '__main__':
    consume_data_from_redis()
