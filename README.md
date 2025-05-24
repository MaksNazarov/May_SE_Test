# CLI-Chat

Простое консольное приложение-чат, поддерживающее переключение между каналами/чатами.

### Запуск приложения (локально)

```
# Firstly, we need to start RabbitMQ server:
sudo  docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq

# And after we can run the programm with arguments (name and starting channel)
python3 chat.py --name Alice --channel lobby

```