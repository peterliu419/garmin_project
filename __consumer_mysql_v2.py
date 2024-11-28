import redis
import json
import mysql.connector
import logging
import time

class StreamConsumer:
    def __init__(self, redis_host='localhost', mysql_config=None):
        # Redis connection
        self.redis_client = redis.Redis(host=redis_host)
        
        # MySQL configuration
        self.mysql_config = mysql_config

        # Stream configuration
        self.STREAM_NAME = 'activity_stream'
        self.CONSUMER_GROUP = 'activity_processors'
        self.CONSUMER_NAME = 'consumer_1'
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def initialize_stream(self):
        """Ensure consumer group exists"""
        try:
            # Create consumer group if not exists
            self.redis_client.xgroup_create(
                self.STREAM_NAME, 
                self.CONSUMER_GROUP, 
                id='0', 
                mkstream=True
            )
            self.logger.info("Stream and consumer group initialized")
        except redis.exceptions.ResponseError:
            self.logger.info("Consumer group already exists")

    def check_redis_stream(self):
        """Check the current state of the Redis stream"""
        try:
            # Get stream length
            stream_length = self.redis_client.xlen(self.STREAM_NAME)
            self.logger.info(f"Current stream length: {stream_length} messages")
            return stream_length
        except Exception as e:
            self.logger.error(f"Error checking Redis stream: {e}")
            return 0

    def process_message(self, message):
        """Process individual message and store in MySQL"""
        try:
            # Extract message data
            message_id, message_data = message
            activity_log = json.loads(message_data[b'data'])

            # MySQL connection and insertion logic
            with mysql.connector.connect(**self.mysql_config) as conn:
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO activities 
                    (user_id, activity_type, timestamp, duration, distance, 
                     heart_rate, calories_burned, latitude, longitude, 
                     device_id, activity_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        activity_log['user_id'],
                        activity_log['activity_type'],
                        activity_log['timestamp'],
                        activity_log.get('duration', 0),
                        activity_log.get('distance', 0),
                        activity_log.get('heart_rate', 0),
                        activity_log.get('calories_burned', 0),
                        activity_log['location']['latitude'],
                        activity_log['location']['longitude'],
                        activity_log.get('device_id', ''),
                        activity_log.get('activity_status', 'pending')
                    )
                    
                    cursor.execute(query, values)
                    conn.commit()

                    self.logger.info(f"✅ Successfully processed message: {message_id}")
                    return message_id

        except Exception as e:
            self.logger.error(f"❌ Processing error for message: {e}")
            return None

    def consume_messages(self, block=2000, count=10):
        """
        Consume messages with advanced error handling
        """
        self.initialize_stream()

        # Initial stream check
        initial_stream_length = self.check_redis_stream()
        self.logger.info(f"Starting consumption with {initial_stream_length} messages in stream")

        while True:
            try:
                # Read messages for this consumer group
                messages = self.redis_client.xreadgroup(
                    groupname=self.CONSUMER_GROUP,
                    consumername=self.CONSUMER_NAME,
                    streams={self.STREAM_NAME: '>'},  # Read new messages
                    count=count,
                    block=block
                )

                if not messages:
                    self.logger.info("No new messages. Waiting...")
                    time.sleep(2)
                    continue

                self.logger.info(f"Received {len(messages[0][1])} messages to process")

                for _, stream_messages in messages:
                    for message in stream_messages:
                        processed_id = self.process_message(message)
                        
                        if processed_id:
                            # Acknowledge successful processing
                            self.redis_client.xack(
                                self.STREAM_NAME, 
                                self.CONSUMER_GROUP, 
                                processed_id
                            )
                        else:
                            self.logger.warning(f"Failed to process message: {message}")

            except Exception as e:
                self.logger.error(f"Consumption error: {e}")
                time.sleep(2)

if __name__ == '__main__':
    consumer = StreamConsumer()
    consumer.consume_messages()