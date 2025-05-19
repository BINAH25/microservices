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
import os

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

# Setup Jaeger exporter
resource = Resource({SERVICE_NAME: "flask_service"})
jaeger_exporter = JaegerExporter(
    agent_host_name="13.58.193.105",  # Replace with your Jaeger agent's IP
    agent_port=6831,
)
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(jaeger_exporter))

# Initialize Flask app and instrumentation
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

def get_database_secrets():
    current_region = "us-east-2"
    secret_name = "my-flask-db-secret-us-east-2"

    try:
        print(f"Fetching secret: {secret_name}")
        client = boto3.client("secretsmanager", region_name=current_region)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        print(f"Failed to fetch secret: {e}")
        raise RuntimeError("Could not retrieve DB credentials")
        
secrets = get_database_secrets()

# Database configuration
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

# Model Definitions
@dataclass
class Product(db.Model):
    id: int 
    title: str 
    image: str 

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
