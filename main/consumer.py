import pika, json
from main import app, Product, db  
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
import os
# Match the same service name
resource = Resource(attributes={
    SERVICE_NAME: "flask_service"  # Same as main.py
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()
jeager_url = os.environ.get("JAEGAR_URL")
jeager_port = os.environ.get("JAEGAR_PORT")

rabbit_mq_url = os.environ.get("RABBIT_MQ_URL")


jaeger_exporter = JaegerExporter(
    agent_host_name=jeager_url,
    agent_port=jeager_port,
)
tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Now get the tracer
tracer = trace.get_tracer(__name__)

params = pika.URLParameters(rabbit_mq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    ctx = TraceContextTextMapPropagator().extract(properties.headers or {})

    with tracer.start_as_current_span("process_message", context=ctx):
        with app.app_context():
            if properties.content_type == 'product_created':
                product = Product(id=data['id'], title=data['title'], image=data['image'])
                db.session.add(product)
                db.session.commit()
                print('Product Created')

            elif properties.content_type == 'product_updated':
                product = Product.query.get(data['id'])
                product.title = data['title']
                product.image = data['image']
                db.session.commit()
                print('Product Updated')

            elif properties.content_type == 'product_deleted':
                product = Product.query.get(data)
                db.session.delete(product)
                db.session.commit()
                print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()
channel.close()
