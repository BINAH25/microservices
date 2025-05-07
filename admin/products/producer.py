import pika, json

params = pika.URLParameters('amqps://egqukmzy:2tO7ORPNQcC8O3fQ1B5QAbluJi5GG7il@beaver.rmq.cloudamqp.com/egqukmzy')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
