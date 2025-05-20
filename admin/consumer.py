import pika, json, os, django
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.context import attach, detach
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

# Configure Tracer Provider
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource({SERVICE_NAME: "django-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="13.58.193.105",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

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

