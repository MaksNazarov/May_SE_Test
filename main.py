import argparse
import pika
import threading
import sys


INITIAL_CHANNEL = "main"

current_channel = INITIAL_CHANNEL
consumer_thread = None
stop_event = threading.Event()


def consumer(channel_name):
    """Create a short-lived connection to the channel and set up required print callback."""
    global stop_event

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()
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


def switch_channel(new_channel):
    """Stop current consumer and create a new one for different channel."""
    global consumer_thread, current_channel, stop_event

    print(f"Switching to channel [{new_channel}]...")

    if consumer_thread and consumer_thread.is_alive():
        stop_event.set()
        consumer_thread.join(timeout=1)

    stop_event.clear()
    current_channel = new_channel

    consumer_thread = threading.Thread(target=consumer, args=(current_channel,))
    consumer_thread.daemon = True
    consumer_thread.start()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="user")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    switch_channel(INITIAL_CHANNEL) # set up consumer for default channel

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()
    channel.exchange_declare(INITIAL_CHANNEL, 'fanout') # connect to default channel

    print(f"Welcome to channel [{current_channel}]!")
    try:
        while True:
            try:
                msg = input().strip()
                if msg.startswith("!switch"): # switch channel
                    _, new_channel = msg.split(maxsplit=1)
                    switch_channel(new_channel)
                else: # broadcast passed message to a current channel
                    channel.basic_publish(
                        exchange=current_channel,
                        routing_key='',
                        body=f"[{args.username}] {msg}".encode()
                    )
            except ValueError:
                print("Usage: !switch <channel>")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_event.set() # stop signal for consumer thread
        if consumer_thread:
            consumer_thread.join(timeout=1)
        conn.close()
        print("Session ended")
        sys.exit(0)