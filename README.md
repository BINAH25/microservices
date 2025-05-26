# Python Microservices Architecture

This project implements a microservices architecture using Python, featuring two main services: a Flask-based main service and a Django-based admin service. The system uses RabbitMQ for message queuing and MySQL for data persistence.

## Content
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
  - [Main Service](#main-service)
  - [Admin Service](#admin-service)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Running with Docker Compose](#running-with-docker-compose)
  - [Manual Setup](#manual-setup)
- [API Documentation](#api-documentation)
  - [Main Service (Port 5000)](#main-service-port-5000)
  - [Admin Service (Port 8000)](#admin-service-port-8000)
- [AWS Secrets Manager Integration](#aws-secrets-manager-integration)
- [Monitoring and Observability](#monitoring-and-observability)
  - [Metrics Collection](#metrics-collection)
  - [OpenTelemetry](#opentelemetry)
  - [Health Checks](#health-checks)
- [Message Queue Architecture](#message-queue-architecture)
- [Database Schema](#database-schema)
  - [Main Service](#database-schema-main-service)
  - [Admin Service](#database-schema-admin-service)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Development Guidelines](#development-guidelines)
- [Contributing](#contributing)
- [Authors](#authors)
- [Support](#support)

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
- **Framework**: Flask 1.1.2+
- **ORM**: SQLAlchemy 1.3.20+
- **Database Migration**: Flask-Migrate
- **Cross-Origin Support**: Flask-CORS
- **Message Queue Client**: Pika 1.1.0+ (RabbitMQ client)
- **Monitoring**: Prometheus Flask Exporter
- **Database Driver**: PyMySQL
- **AWS Integration**: Boto3 (AWS SDK)
- **WSGI Server**: Gunicorn

#### Core Components

1. **API Server (`main.py`)**
   - RESTful API endpoints for product management
   - Database connection with AWS Secrets Manager integration
   - CORS support for cross-origin requests
   - Prometheus metrics for monitoring
   - Health check endpoint at `/flask/api/health`

2. **Message Producer (`producer.py`)**
   - Handles publishing messages to RabbitMQ
   - Supports product like events
   - Uses CloudAMQP as the message broker
   - Implements proper connection handling and error recovery

3. **Message Consumer (`consumer.py`)**
   - Listens to the 'main' queue for events from the Admin service
   - Processes product creation, update, and deletion events
   - Updates local database based on received messages
   - Implements message acknowledgment for reliability

4. **Data Models**
   - `Product`: Stores product information (id, title, image)
   - `ProductUser`: Tracks user likes for products with unique constraints

#### API Endpoints

- **GET** `/flask/api/products`: Retrieves all products
  - Response: JSON array of product objects
  - Status codes: 200 (Success)

- **POST** `/flask/api/products/<id>/like`: Likes a product
  - Path parameter: `id` (Product ID)
  - Response: Success message
  - Status codes: 200 (Success), 400 (Already liked), 404 (Not found)

- **GET** `/flask/api/health`: Health check endpoint
  - Response: Service health status including database connection
  - Status codes: 200 (Healthy), 500 (Unhealthy)

#### Deployment Configuration

- Docker containerization with separate services:
  - `flask_backend`: Main API service
  - `queue`: Message consumer service
  - `db`: MySQL database service
- Persistent volume for database data
- Shared network for inter-service communication
- Automated database migration using Flask-Migrate
- Gunicorn WSGI server for production deployment
- Non-root user execution for queue consumer (security best practice)

#### Security Features

- AWS Secrets Manager integration for secure database credential storage
- Fallback to environment variables when AWS Secrets Manager is unavailable
- Containerized services with minimal dependencies using Alpine Linux
- Security headers through Flask-CORS configuration
- Non-root user execution for message queue consumers
- Secure connection to CloudAMQP using AMQPS protocol

#### High Availability and Scaling

- Stateless application design for horizontal scaling
- Health check endpoint for container orchestration monitoring
- Prometheus metrics for performance monitoring and alerting
- Containerized architecture supporting orchestration with Kubernetes or ECS
- Database connection error handling with graceful degradation

### Admin Service
- **Framework**: Django 3.1.3+
- **API Framework**: Django REST Framework 3.12.2+
- **Database Adapter**: Django MySQL 3.9+
- **Cross-Origin Support**: Django CORS Headers 3.5.0+
- **Message Queue Client**: Pika 1.1.0+ (RabbitMQ client)
- **Observability**: OpenTelemetry with OTLP exporter
- **Monitoring**: Prometheus Client with django-prometheus
- **WSGI Server**: Gunicorn 21.2.0+
- **AWS Integration**: Boto3 (AWS SDK)

#### Core Components

1. **Django Application (`admin/`)**
   - Django admin interface for backend management
   - AWS Secrets Manager integration for database credentials
   - OpenTelemetry instrumentation for distributed tracing
   - Prometheus metrics for monitoring via django-prometheus
   - CORS configuration for frontend integration

2. **Products Module (`products/`)**
   - RESTful API using Django REST Framework
   - Product data model with serialization
   - ViewSets for CRUD operations
   - Random user selection for testing/simulation

3. **Message Producer (`products/producer.py`)**
   - Publishes events to RabbitMQ when products are created, updated, or deleted
   - Communicates with the Main service via the 'main' queue
   - Uses CloudAMQP as the message broker
   - Implements proper error handling and connection management

4. **Message Consumer (`consumer.py`)**
   - Listens to the 'admin' queue for events from the Main service
   - Processes product like events
   - Updates product like counts in the database
   - Implements message acknowledgment for reliability

5. **Data Models**
   - `Product`: Stores product information (title, image, likes)
   - Uses Django ORM for database interactions

#### API Endpoints

- **GET** `/api/products`: Lists all products
  - Response: JSON array of product objects
  - Status codes: 200 (Success)

- **POST** `/api/products`: Creates a new product
  - Request body: JSON object with product details
  - Response: Created product with ID
  - Status codes: 201 (Created), 400 (Bad Request)

- **GET** `/api/products/<id>`: Retrieves a specific product
  - Path parameter: `id` (Product ID)
  - Response: Product details
  - Status codes: 200 (Success), 404 (Not Found)

- **PUT** `/api/products/<id>`: Updates a product
  - Path parameter: `id` (Product ID)
  - Request body: JSON object with updated product details
  - Response: Updated product
  - Status codes: 202 (Accepted), 400 (Bad Request), 404 (Not Found)

- **DELETE** `/api/products/<id>`: Deletes a product
  - Path parameter: `id` (Product ID)
  - Response: Empty response
  - Status codes: 204 (No Content), 404 (Not Found)

- **GET** `/api/user`: Returns a random user ID
  - Response: User ID
  - Status codes: 200 (Success), 404 (Not Found)

- **GET** `/metrics`: Prometheus metrics endpoint
  - Response: Prometheus metrics in text format
  - Status codes: 200 (Success)

#### Security Features

- AWS Secrets Manager integration for secure database credential storage
- Non-root user execution in Docker containers
- Secure connection to CloudAMQP using AMQPS protocol
- Django security middleware configuration
- CORS configuration with proper headers

#### Monitoring and Observability

- OpenTelemetry instrumentation for distributed tracing
- Prometheus metrics for monitoring Django performance
- Middleware for tracking request durations and counts
- Support for custom application metrics

#### Deployment Configuration

- Docker containerization with Alpine Linux base for minimal footprint
- Separate containers for the Django application and message consumer
- PostgreSQL database integration with persistent storage
- Static file management with dedicated volume
- Security-focused container configuration with non-root user execution
- Entrypoint script for database migrations and application startup
- Gunicorn WSGI server for production deployment

#### Architecture Patterns

- Repository pattern through Django ORM
- Adapter pattern for external service integration
- Observer pattern via message queue notifications
- Dependency injection for AWS Secrets Manager and database configuration
- Circuit breaker pattern for external service calls
- Microservice event choreography with RabbitMQ

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
   git clone https://github.com/BINAH25/python-microservices.git
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
