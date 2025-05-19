import pika, json
from opentelemetry import trace
from opentelemetry.trace import set_span_in_context

# Initialize tracer
tracer = trace.get_tracer(__name__)

def publish(method, body):
    params = pika.URLParameters('amqps://egqukmzy:2tO7ORPNQcC8O3fQ1B5QAbluJi5GG7il@beaver.rmq.cloudamqp.com/egqukmzy')

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Start a new span for publishing the message
        with tracer.start_as_current_span("publish_message") as span:
            properties = pika.BasicProperties(
                method,
                headers=span.context.to_headers()  # Propagate trace context here
            )

            channel.basic_publish(
                exchange='',
                routing_key='admin',
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
