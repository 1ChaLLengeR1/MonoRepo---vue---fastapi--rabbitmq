import pika
import json
import threading
import time
from repository.create import create_user_psql
from repository.update import update_user_psql
from repository.delete import delete_user_psql


class RabbitMQConsumer:
    def __init__(self, host='rabbitmq', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.should_stop = False

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
            connection_attempts=3,
            retry_delay=2.0,
            socket_timeout=10.0
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare queue
        self.channel.queue_declare(queue='user.sync', durable=True)

        # Set QoS to process one message at a time
        self.channel.basic_qos(prefetch_count=1)

    def process_message(self, channel, method, properties, body):
        try:
            message = json.loads(body.decode('utf-8'))
            action = message.get('action')
            user_data = message.get('user_data', {})

            print(f"Processing {action} message: {user_data}")

            if action == 'create':
                result = create_user_psql(
                    name=user_data.get('name'),
                    lastname=user_data.get('lastname'),
                    email=user_data.get('email'),
                    age=user_data.get('age'),
                    city=user_data.get('city')
                )
                print(f"Create result: {result}")

            elif action == 'update':
                result = update_user_psql(
                    user_id=user_data.get('id'),
                    name=user_data.get('name'),
                    lastname=user_data.get('lastname'),
                    email=user_data.get('email'),
                    age=user_data.get('age'),
                    city=user_data.get('city')
                )
                result = update_user_psql(result)
                print(f"Update result: {result}")

            elif action == 'delete':
                result = delete_user_psql(email=user_data.get('email'))
                print(f"Delete result: {result}")

            # Acknowledge the message
            channel.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # Reject the message and don't requeue it
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming_with_reconnect(self):
        """
        Start consuming with automatic reconnection logic
        """
        reconnect_delay = 5.0

        while not self.should_stop:
            try:
                print("Connecting to RabbitMQ...")
                self.connect()

                self.channel.basic_consume(
                    queue='user.sync',
                    on_message_callback=self.process_message
                )

                print('✅ RabbitMQ consumer connected and waiting for messages...')
                self.channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                print(f"❌ Connection lost: {str(e)}")
                if not self.should_stop:
                    print(f"🔄 Reconnecting in {reconnect_delay} seconds...")
                    time.sleep(reconnect_delay)
                    reconnect_delay = min(reconnect_delay * 1.5, 60)  # Max 60s delay

            except KeyboardInterrupt:
                print('🛑 Stopping consumer...')
                self.should_stop = True

            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                if not self.should_stop:
                    print(f"🔄 Reconnecting in {reconnect_delay} seconds...")
                    time.sleep(reconnect_delay)

            finally:
                try:
                    if self.channel and not self.channel.is_closed:
                        self.channel.stop_consuming()
                    if self.connection and not self.connection.is_closed:
                        self.connection.close()
                except:
                    pass

                # Reset connection state
                self.connection = None
                self.channel = None

    def stop(self):
        self.should_stop = True
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except:
            pass


def start_consumer_thread():
    consumer = RabbitMQConsumer()
    consumer_thread = threading.Thread(target=consumer.start_consuming_with_reconnect, daemon=True)
    consumer_thread.start()
    return consumer_thread, consumer


if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.start_consuming_with_reconnect()
