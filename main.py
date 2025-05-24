import argparse
import pika
import threading
import sys


MAIN_CHANNEL_NAME = "main"
stop_event = threading.Event()


def consumer():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()

    channel_name = MAIN_CHANNEL_NAME
    channel.exchange_declare(channel_name, 'fanout')
    queue = channel.queue_declare('', exclusive=True).method.queue
    channel.queue_bind(queue, channel_name)

    def callback(channel, method, properties, body):
        print(f"[{channel_name}] {body.decode()}")

    channel.basic_consume(queue, callback, auto_ack=True)

    print(f"Listening to [{channel_name}]...")

    try:
        while not stop_event.is_set():
            conn.process_data_events(time_limit=1)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="user")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()
    channel.exchange_declare(MAIN_CHANNEL_NAME, 'fanout')

    print(f"Welcome to channel [{MAIN_CHANNEL_NAME}]! (Press Ctrl+C to exit)")
    try:
        while True:
            msg = input()
            channel.basic_publish(MAIN_CHANNEL_NAME, '', f"[{args.username}] {msg}".encode())
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_event.set()
        consumer_thread.join(timeout=1)
        conn.close()
        print("Session ended")
        sys.exit(0)