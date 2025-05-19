import pika, json
from main import app, Product, db
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.context import attach, detach

# Initialize tracer
tracer = trace.get_tracer(__name__)

params = pika.URLParameters('amqps://egqukmzy:2tO7ORPNQcC8O3fQ1B5QAbluJi5GG7il@beaver.rmq.cloudamqp.com/egqukmzy')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    with app.app_context(): 
        # Extract trace context from message headers
        context = TraceContextTextMapPropagator().extract(properties.headers or {})

        with tracer.start_as_current_span("process_message", context=context):
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
