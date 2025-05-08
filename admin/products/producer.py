import pika, json

def publish(method, body):
    params = pika.URLParameters('amqps://egqukmzy:2tO7ORPNQcC8O3fQ1B5QAbluJi5GG7il@beaver.rmq.cloudamqp.com/egqukmzy')

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        properties = pika.BasicProperties(method)
        channel.basic_publish(
            exchange='',
            routing_key='main',
            body=json.dumps(body),
            properties=properties
        )
    except Exception as e:
        print('RabbitMQ publish error:', e)
    finally:
        try:
            connection.close()
        except:
            pass
