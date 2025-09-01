import pika
import json
import time
from datetime import datetime


def publish_message_with_retry(action: str, user_data: dict,  max_retries: int = 3, retry_delay: float = 1.0):
    """
    Publish message with retry logic using short-lived connections
    """
    message = {
        "action": action,
        "user_data": user_data,
        "timestamp": datetime.now().isoformat()
    }
    
    for attempt in range(max_retries):
        connection = None
        try:
            # Create new connection for each publish
            credentials = pika.PlainCredentials('guest', 'guest')
            parameters = pika.ConnectionParameters(
                host='rabbitmq',
                port=5672,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=1.0,
                socket_timeout=10.0
            )
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            # Declare queue (idempotent)
            channel.queue_declare(queue='user.sync', durable=True)
            
            # Publish message
            channel.basic_publish(
                exchange='',
                routing_key='user.sync',
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            
            print(f"Successfully published {action} message for user: {user_data.get('id', 'unknown')}")
            return True
            
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
        finally:
            if connection and not connection.is_closed:
                try:
                    connection.close()
                except:
                    pass
    
    print(f"Failed to publish {action} message after {max_retries} attempts")
    return False


def publish_user_created(user_data: dict):
    publish_message_with_retry("create", user_data)


def publish_user_updated(user_data: dict):
    publish_message_with_retry("update", user_data)


def publish_user_deleted(user_id: str):
    user_data = {"id": user_id}
    publish_message_with_retry("delete", user_data)