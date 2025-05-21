# Python Microservices Architecture

This project implements a microservices architecture using Python, featuring two main services: a Flask-based main service and a Django-based admin service. The system uses RabbitMQ for message queuing and MySQL for data persistence.

## Architecture Overview

The project consists of two main microservices:

1. **Main Service** (Flask-based)
   - RESTful API endpoints for product management
   - Producer-Consumer pattern implementation with RabbitMQ
   - MySQL database integration
   - Prometheus metrics integration for monitoring
   - AWS Secrets Manager integration for database credentials

2. **Admin Service** (Django-based)
   - Admin dashboard and management interface
   - REST API using Django REST Framework
   - Producer-Consumer pattern implementation with RabbitMQ
   - OpenTelemetry integration for observability
   - Prometheus integration for metrics collection

## Technology Stack

### Main Service
- Flask 1.1.2+
- SQLAlchemy 1.3.20+
- Flask-Migrate
- Flask-CORS
- Pika 1.1.0+ (RabbitMQ client)
- Prometheus Flask Exporter
- PyMySQL
- Boto3 (AWS SDK)
- Gunicorn

### Admin Service
- Django 3.1.3+
- Django REST Framework 3.12.2+
- Django MySQL 3.9+
- Django CORS Headers 3.5.0+
- Pika 1.1.0+ (RabbitMQ client)
- OpenTelemetry
- Prometheus Client
- Gunicorn 21.2.0+

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- MySQL 8.0
- RabbitMQ
- AWS account (for Secrets Manager)

## Project Structure

```
.
├── admin/                    # Admin service (Django)
│   ├── admin/               # Django admin app configuration
│   ├── products/            # Products module with models and APIs
│   ├── consumer.py          # Message consumer for RabbitMQ
│   ├── Dockerfile           # Docker configuration for the service
│   ├── Dockerfile.queue     # Docker configuration for the consumer
│   ├── manage.py            # Django management script
│   ├── requirements.txt     # Python dependencies
│   └── docker-compose.yml   # Docker configuration
│
├── main/                    # Main service (Flask)
│   ├── main.py             # Main application
│   ├── producer.py         # Message producer for RabbitMQ
│   ├── consumer.py         # Message consumer
│   ├── Dockerfile          # Docker configuration for the service
│   ├── Dockerfile.queue    # Docker configuration for the consumer
│   ├── requirements.txt    # Python dependencies
│   └── docker-compose.yml  # Docker configuration
│
├── Jenkinsfile             # CI/CD pipeline configuration
└── .gitignore             # Git ignore rules
```

## Getting Started

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-microservices-1.git
   cd python-microservices-1
   ```

2. Create the shared network:
   ```bash
   docker network create shared-network
   ```

3. Start the main service:
   ```bash
   cd main
   docker-compose up --build
   ```

4. Start the admin service:
   ```bash
   cd admin
   docker-compose up --build
   ```

### Manual Setup

1. Set up Python virtual environments:
   ```bash
   # For main service
   cd main
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # For admin service
   cd admin
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure environment variables:

   **Main Service:**
   ```
   SQL_USER=user
   SQL_PASSWORD=password
   SQL_HOST=localhost
   SQL_PORT=3306
   SQL_DATABASE=main
   ```

   **Admin Service:**
   ```
   DJANGO_SETTINGS_MODULE=admin.settings
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=admin
   SQL_USER=user
   SQL_PASSWORD=password
   SQL_HOST=localhost
   SQL_PORT=3306
   ```

3. Run the services:
   ```bash
   # Main service
   cd main
   python main.py

   # Admin service
   cd admin
   python manage.py runserver
   ```

## API Documentation

### Main Service (Port 5000)
- **GET** `/flask/api/products` - Get all products
- **POST** `/flask/api/products/<id>/like` - Like a product

### Admin Service (Port 8000)
- Django admin interface at `/admin`
- **GET** `/api/products` - List all products
- **POST** `/api/products` - Create a product
- **GET** `/api/products/<id>` - Get a specific product
- **PUT** `/api/products/<id>` - Update a product
- **DELETE** `/api/products/<id>` - Delete a product

## AWS Secrets Manager Integration

The main service uses AWS Secrets Manager to securely store and retrieve database credentials. The service falls back to environment variables if secrets cannot be retrieved.

To set up your own secrets:
1. Create a secret in AWS Secrets Manager named `my-flask-db-secret-us-east-2`
2. Add the following key-value pairs:
   - `username`: Database username
   - `password`: Database password
   - `host`: Database host
   - `port`: Database port
   - `dbname`: Database name

## Monitoring and Observability

### Metrics Collection
- Prometheus metrics available at `/metrics` for both services
- Main service uses prometheus-flask-exporter
- Admin service uses django-prometheus

### OpenTelemetry
The admin service is instrumented with OpenTelemetry for distributed tracing.

### Health Checks
- Main service: `/flask/api/health`
- Admin service: `/api/health`

## Message Queue Architecture

Both services communicate through RabbitMQ using the following exchanges and queues:

1. **Main Service:**
   - Publishes to `product_liked` exchange when a product is liked
   - Consumes from `admin` queue for updates

2. **Admin Service:**
   - Publishes to `product_created` exchange when a product is created/updated
   - Consumes from `main` queue for updates

## Database Schema

### Main Service
- **Product**: id, title, image
- **ProductUser**: id, user_id, product_id

### Admin Service
- **Product**: id, title, image, likes
- **User**: id, name, email

## CI/CD Pipeline

The project includes a Jenkins pipeline that:
- Builds and tests the application
- Runs security scans
- Deploys to staging/production environments
- Performs database migrations

## Troubleshooting

### Common Issues
1. **Database Connection Issues**
   - Verify database credentials
   - Ensure the MySQL service is running
   - Check network connectivity

2. **RabbitMQ Connection Issues**
   - Verify RabbitMQ is running
   - Check connection parameters
   - Ensure queues and exchanges are properly declared

3. **Docker Network Issues**
   - Ensure `shared-network` is created
   - Check container logs for network-related errors

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Write docstrings for all functions and classes

2. **Testing**
   - Write unit tests for new features
   - Maintain test coverage above 80%
   - Run tests before committing

3. **Documentation**
   - Update API documentation when making changes
   - Document new environment variables
   - Keep README up to date

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Authors

- Louis Binah <louisbinah@gmail.com>
- Yaw Mintah <yawmintah@gmail.com>
- Michael Oppong <michaeloppong731@gmail.com>
- Hamdani Alhassan Gandi <hamdanialhassangandi2020@gmail.com>

<!-- ## License

This project is licensed under the MIT License - see the LICENSE file for details. -->

## Support

For support or questions, please contact:
- Louis Binah <louisbinah@gmail.com>
- Open an issue on the repository
