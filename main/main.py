import os
from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
from prometheus_flask_exporter import PrometheusMetrics
from producer import publish
import boto3
import json
from botocore.exceptions import ClientError

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

# Set up tracing
resource = Resource(attributes={SERVICE_NAME: "flask_service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
jeager_url = os.environ.get("JAEGAR_URL")
jeager_port = os.environ.get("JAEGAR_PORT")
rabbit_mq_url = os.environ.get("RABBIT_MQ_URL")

jaeger_exporter = JaegerExporter(
    agent_host_name=jeager_url,
    agent_port=6831,
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)

# --- Flask App Setup ---
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, tracer_provider=provider)
RequestsInstrumentor().instrument()

current_region = os.environ.get("AWS_REGION")
secret_name = os.environ.get("SECRET_NAME")

if not current_region or not secret_name:
    raise RuntimeError("Missing required environment variables: AWS_REGION or DB_SECRET_NAME")


def get_database_secrets():
   
    try:
        print(f"Fetching secret: {secret_name}")
        client = boto3.client("secretsmanager", region_name=current_region)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        print(f"Failed to fetch secret: {e}")
        raise RuntimeError("Could not retrieve DB credentials")
secrets = get_database_secrets()

db_user = secrets.get("username", os.environ.get("SQL_USER", "user"))
db_password = secrets.get("password", os.environ.get("SQL_PASSWORD", "password"))
db_host = secrets.get("host", os.environ.get("SQL_HOST", "localhost"))
db_port = secrets.get("port", os.environ.get("SQL_PORT", "3306"))
db_name = secrets.get("dbname", os.environ.get("SQL_DATABASE", "main"))


app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
CORS(app)
metrics = PrometheusMetrics(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    # for serializing into json
    id: int 
    title: str 
    image: str 

    # for db
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) # product_id created in django
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    # no likes -> in django

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # not sure if working ?
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/flask/api/products')
def index():
    with tracer.start_as_current_span("get_all_products"):
        return jsonify(db.session.query(Product).all())

@app.route('/flask/api/products/<int:id>/like', methods=['POST'])
def like(id):
    with tracer.start_as_current_span("like_product"):
        req = requests.get('https://django.seyram.site/api/user')
        json_data = req.json()

    try:
        product_user = ProductUser(user_id=json_data['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        publish('product_liked', id)
    except Exception as e:
        print(e)
        abort(400, 'You already liked this product.')

    return jsonify({
        'message': 'success'
    })

@app.route('/ready')
def readiness_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')