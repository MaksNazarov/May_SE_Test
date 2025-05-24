import argparse


MAIN_CHANNEL_NAME = "main"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="user")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    print(f"Welcome to channel [{MAIN_CHANNEL_NAME}]!")
    while True:
        msg = input()
        print(f"{args.username} says: {msg}")
