# May_SE_Test

This project is a small RabbitMQ-based console chat with channel subscription feature.


# Requirements

1. RabbitMQ:
To install it, first, make sure you have Docker available on your machine.
Then, run from console:
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

2. Python 3.7+
3. [Pika](https://pypi.org/project/pika/) library for Python


# How to run

1. Start RabbitMQ container.
2. Switch to your virtual Python environment
3. Enter the project directory
4. Run
    ```
    pip install -r requirements.txt
    ```
    to install project Python dependencies
5. Run
    ```
    python client_chat.py --username your_desired_username
    ```