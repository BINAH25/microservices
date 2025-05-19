import pika, json, os, django
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.context import attach, detach

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

# Get the tracer
tracer = trace.get_tracer(__name__)

params = pika.URLParameters('amqps://egqukmzy:2tO7ORPNQcC8O3fQ1B5QAbluJi5GG7il@beaver.rmq.cloudamqp.com/egqukmzy')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    # Extract trace context from message headers
    context = TraceContextTextMapPropagator().extract(properties.headers or {})

    with tracer.start_as_current_span("process_message", context=context):
        print('Received in admin')
        id = json.loads(body)
        print(id)
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        product.save()
        print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')
channel.start_consuming()

channel.close()
