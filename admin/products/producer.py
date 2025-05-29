import pika, json
from opentelemetry import trace
from opentelemetry.context import get_current
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import os
# Get the tracer
tracer = trace.get_tracer(__name__)
rabbit_mq_url = os.environ.get("RABBIT_MQ_URL")

def publish(method, body):
    params = pika.URLParameters(rabbit_mq_url)

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        with tracer.start_as_current_span("publish_message") as span:
            headers = {}
            # Inject trace context into headers
            TraceContextTextMapPropagator().inject(carrier=headers, context=get_current())

            properties = pika.BasicProperties(
                content_type=method,
                headers=headers  # Propagate trace context here
            )

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
