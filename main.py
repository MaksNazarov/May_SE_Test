import argparse
import pika
import threading


MAIN_CHANNEL_NAME = "main"


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
    channel.start_consuming()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="user")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    threading.Thread(target=consumer).start()

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()
    channel.exchange_declare(MAIN_CHANNEL_NAME, 'fanout')

    print(f"Welcome to channel [{MAIN_CHANNEL_NAME}]!")
    while True:
        try:
            msg = input()
            channel.basic_publish(MAIN_CHANNEL_NAME, '', f"[{args.username}] {msg}".encode())
        except KeyboardInterrupt:
            print("\nSession ended")
            break
