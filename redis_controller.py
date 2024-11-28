import redis
import json
import logging

# Add logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RedisController:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.r = redis.Redis(host=host, port=port, db=db)
            # Verify connection
            self.r.ping()
            logging.info(f"Successfully connected to Redis at {host}:{port}")
            self.key = "activity_logs"
        except redis.ConnectionError as e:
            logging.error(f"Failed to connect to Redis: {e}")
            raise

    def check_redis_data(self, max_logs=100):
        try:
            length = self.r.llen(self.key)
            logging.info(f"Number of activity logs in Redis: {length}")

            if length > 0:
                # Limit number of logs to prevent overwhelming output
                activity_logs = self.r.lrange(self.key, 0, max_logs - 1)
                
                for idx, log_data in enumerate(activity_logs, 1):
                    try:
                        activity_log = json.loads(log_data)
                        logging.info(f"Log {idx}: {json.dumps(activity_log, indent=2)}")
                    except json.JSONDecodeError:
                        logging.warning(f"Could not decode log {idx}")
            else:
                logging.info("No activity logs found in Redis.")
        
        except Exception as e:
            logging.error(f"Error checking Redis data: {e}")

    def clear_redis_data(self):
        try:
            confirmation = input("Are you sure you want to delete all activity logs from Redis? (y/n): ")
            if confirmation.lower() == 'y':
                deleted_count = self.r.delete(self.key)
                logging.info(f"Deleted {deleted_count} activity log list(s).")
            else:
                logging.info("No data was deleted.")
        
        except Exception as e:
            logging.error(f"Error clearing Redis data: {e}")

    def monitor_redis_size(self):
        """Monitor and log Redis list size"""
        try:
            current_size = self.r.llen(self.key)
            logging.info(f"Current Redis activity log list size: {current_size}")
            return current_size
        except Exception as e:
            logging.error(f"Error monitoring Redis list size: {e}")
            return None

if __name__ == '__main__':
    try:
        controller = RedisController()
        controller.check_redis_data()
        
        # Optional: Monitor list size
        controller.monitor_redis_size()
        
        # Uncomment to clear data if needed
        # controller.clear_redis_data()
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")