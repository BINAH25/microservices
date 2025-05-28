# Python Microservices Architecture

This project implements a microservices architecture using Python, featuring two main services: a Flask-based main service and a Django-based admin service, along with a React frontend. The system uses RabbitMQ for message queuing and MySQL for data persistence.


## Content
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
  - [Frontend](#frontend)
  - [Main Service](#main-service)
  - [Admin Service](#admin-service)
- [Application Screenshots](#application-screenshots)
  - [Main Service](#screenshots-main-service)
  - [Admin Service](#screenshots-admin-service)
  - [RabbitMQ Dashboard](#screenshots-rabbitmq)
  - [Monitoring Dashboard](#screenshots-monitoring)
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
  - [Grafana and Prometheus Setup](#grafana-and-prometheus-setup)
  - [OpenTelemetry](#opentelemetry)
  - [Health Checks](#health-checks)
- [Message Queue Architecture](#message-queue-architecture)
  - [RabbitMQ Implementation](#rabbitmq-implementation)
  - [Message Flow](#message-flow)
  - [Queue Configuration](#queue-configuration)
  - [Error Handling](#queue-error-handling)
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

The project consists of three main components:

1. **Frontend** (React-based)
   - User interface for product display and interaction
   - Admin interface for product management
   - Responsive design with Bootstrap styling
   - Communicates with both microservices via REST APIs

2. **Main Service** (Flask-based)
   - RESTful API endpoints for product management
   - Producer-Consumer pattern implementation with RabbitMQ
   - MySQL database integration
   - Prometheus metrics integration for monitoring
   - AWS Secrets Manager integration for database credentials

3. **Admin Service** (Django-based)
   - Admin dashboard and management interface
   - REST API using Django REST Framework
   - Producer-Consumer pattern implementation with RabbitMQ
   - OpenTelemetry integration for observability
   - Prometheus integration for metrics collection

## Application Screenshots

### Frontend Screenshots {#}
![frontend](./resources/main.png)
### Main Service {#screenshots-main-service}

![Main Service Products API](./resources/main.png)
*The Main Service Products API displaying a list of products*

![Main Service Health Check](/images/main-service-health.png)
*Health check endpoint showing service status*

![Main Service Metrics](/images/main-service-metrics.png)
*Prometheus metrics exposed by the Main Service*

### Admin Service {#screenshots-admin-service}

![Admin Dashboard](/images/admin-dashboard.png)
*Django Admin dashboard for product management*

![Admin Service API](/images/admin-service-api.png)
*Admin Service REST API for products*

![Admin Service Metrics](/images/admin-metrics.png)
*Prometheus metrics for the Admin Service*

### RabbitMQ Dashboard {#screenshots-rabbitmq}

![RabbitMQ Overview](/images/rabbitmq-overview.png)
*CloudAMQP RabbitMQ management dashboard overview*

![Message Queues](/images/rabbitmq-queues.png)
*Active queues with message counts and consumers*

![Message Flow](/images/rabbitmq-flow.png)
*Message flow visualization between services*

### Monitoring Dashboard {#screenshots-monitoring}

![Grafana Dashboard - Django](./resources/grafana-django.png)
*Grafana dashboard showing service metrics*

![Prometheus Targets](/images/prometheus-targets.png)
*Prometheus targets showing scrape status*

![Service Metrics](/images/service-metrics.png)
*Detailed service performance metrics*

## Technology Stack

### Frontend
- **Framework**: React 18.2.0+
- **Routing**: React Router DOM 6.8.1+
- **Language**: TypeScript 4.9.5+
- **Build Tool**: Create React App
- **Styling**: Bootstrap CSS
- **Deployment**: Nginx with Docker
- **HTTP Client**: Native Fetch API

#### Core Components

1. **Main Interface (`/src/main/`)**
   - Product display with image gallery format
   - Like functionality that communicates with Main Service
   - Responsive grid layout using Bootstrap
   - Real-time UI updates after like actions

2. **Admin Interface (`/src/admin/`)**
   - Product management dashboard with CRUD operations
   - Product listing with image preview
   - Create/Edit forms with input validation
   - Delete confirmation dialogs
   - Styled admin layout with navigation

3. **Shared Components**
   - Navigation bar with routing links
   - Wrapper component for consistent layouts
   - TypeScript interfaces for type safety
   - Environment-based configuration

4. **API Integration**
   - Communicates with Admin Service for product management
   - Communicates with Main Service for like functionality
   - Fetches data using async/await pattern
   - JSON-based data exchange

#### Frontend Architecture

- **Component-Based Design**: Modular React components with specific responsibilities
- **TypeScript Integration**: Type-safe code with interfaces for data models
- **React Router**: Client-side routing for SPA experience
- **RESTful API Integration**: Direct communication with backend microservices
- **Responsive Design**: Mobile-friendly UI with Bootstrap
- **Docker Deployment**: Nginx-based containerized deployment

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
├── frontend/                 # Frontend application
│   └── microservices-react-main/  # React application
│       ├── react-crud/      # React application code
│       │   ├── src/         # Source code
│       │   │   ├── admin/   # Admin interface components
│       │   │   │   ├── Products.tsx         # Product listing page
│       │   │   │   ├── ProductsCreate.tsx   # Product creation form
│       │   │   │   ├── ProductsEdit.tsx     # Product editing form
│       │   │   │   └── Wrapper.tsx          # Admin layout wrapper
│       │   │   ├── main/    # Main interface components
│       │   │   │   └── Main.tsx             # Main product gallery
│       │   │   ├── interfaces/ # TypeScript interfaces
│       │   │   │   └── product.ts           # Product data model
│       │   │   ├── App.tsx  # Main application component with routing
│       │   │   └── constant.tsx # API endpoint configuration
│       │   ├── Dockerfile   # Docker configuration for frontend
│       │   ├── nginx.conf   # Nginx configuration
│       │   └── package.json # Dependencies and scripts
│       └── docker-compose.yml # Docker configuration for frontend
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
├── grafana-prometheus/      # Monitoring stack
│   ├── prometheus.yml      # Prometheus configuration
│   └── docker-compose.yml  # Docker configuration for monitoring services
│
├── images/                  # Screenshots and diagrams
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

4. Start the admin service<!-- ### Main Service {#screenshots-main-service}

![Main Service Products API](./resources/main.png)
*The Main Service Products API displaying a list of products*

![Main Service Health Check](/images/main-service-health.png)
*Health check endpoint showing service status*

![Main Service Metrics](/images/main-service-metrics.png)
*Prometheus metrics exposed by the Main Service*

### Admin Service {#screenshots-admin-service}

![Admin Dashboard](/images/admin-dashboard.png)
*Django Admin dashboard for product management*

![Admin Service API](/images/admin-service-api.png)
*Admin Service REST API for products*

![Admin Service Metrics](/images/admin-metrics.png)
*Prometheus metrics for the Admin Service*

### RabbitMQ Dashboard {#screenshots-rabbitmq}

![RabbitMQ Overview](/images/rabbitmq-overview.png)
*CloudAMQP RabbitMQ management dashboard overview*

![Message Queues](/images/rabbitmq-queues.png)
*Active queues with message counts and consumers*

![Message Flow](/images/rabbitmq-flow.png)
*Message flow visualization between services*

### Monitoring Dashboard {#screenshots-monitoring}

![Grafana Dashboard](/images/grafana-dashboard.png)
*Grafana dashboard showing service metrics*

![Prometheus Targets](/images/prometheus-targets.png)
*Prometheus targets showing scrape status*

![Service Metrics](/images/service-metrics.png)
*Detailed service performance metrics*

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
├── grafana-prometheus/      # Monitoring stack
│   ├── prometheus.yml      # Prometheus configuration
│   └── docker-compose.yml  # Docker configuration for monitoring services
│
├── images/                  # Screenshots and diagrams
├── Jenkinsfile             # CI/CD pipeline configuration
└── .gitignore             # Git ignore rules:
   ```bash
   cd admin
   docker-compose up --build
   ```

5. Start the frontend:
   ```bash
   cd frontend/microservices-react-main
   docker-compose up --build
   ```
   Access the frontend at http://localhost:80

6. Start the monitoring stack:
   ```bash
   cd grafana-prometheus
   docker-compose up --build
   ```
   Access Grafana at http://localhost:8080 (default credentials: admin/admin)
   Access Prometheus at http://localhost:9090

### Manual Setup

1. Set up the frontend:
   ```bash
   cd frontend/microservices-react-main/react-crud
   npm install
   npm start
   ```
   The development server will start at http://localhost:3000

2. Set up Python virtual environments:
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
- **GET** `/flask/api/health` - Health check endpoint
- **GET** `/metrics` - Prometheus metrics endpoint

### Admin Service (Port 8000)
- Django admin interface at `/admin`
- **GET** `/api/products` - List all products
- **POST** `/api/products` - Create a product
- **GET** `/api/products/<id>` - Get a specific product
- **PUT** `/api/products/<id>` - Update a product
- **DELETE** `/api/products/<id>` - Delete a product
- **GET** `/api/user` - Get a random user ID
- **GET** `/metrics` - Prometheus metrics endpoint

### Frontend
- **Main UI**: http://localhost:80 - Product display and like functionality
  - **GET** `/` - Home page with product gallery
  - **POST** Action - Like a product (communicates with Main Service)
- **Admin UI**: http://localhost:80/admin/products - Product management interface
  - **GET** `/admin/products` - Product listing page
  - **GET** `/admin/products/create` - Create new product form
  - **GET** `/admin/products/:id/edit` - Edit existing product form
  - All admin pages communicate with Admin Service API

### Monitoring Stack
- Grafana: http://localhost:8080 - Visualization dashboards
- Prometheus: http://localhost:9090 - Metrics and alerts

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

### Grafana and Prometheus Setup
The project includes a dedicated monitoring stack with Grafana and Prometheus:

#### Architecture
- **Prometheus**: Collects and stores metrics from all services
- **Grafana**: Provides visualization dashboards for the collected metrics

#### Configuration
The monitoring stack is configured in the `grafana-prometheus` directory:

- **Prometheus Configuration** (`prometheus.yml`):
  - Scrapes metrics from both microservices (Flask and Django)
  - 15-second scrape interval
  - Configured to access services via domain names (`flask.seyram.site` and `django.seyram.site`)
  - Persistent volume for long-term metrics storage

- **Grafana Configuration**:
  - Pre-configured dashboards for service metrics
  - Exposed on port 80 for easy access
  - Persistent volume for dashboard and user configurations

#### Deployment
To deploy the monitoring stack:
```bash
cd grafana-prometheus
docker-compose up -d
```

Access the interfaces at:
- Grafana: http://localhost:80 (default credentials: admin/admin)
- Prometheus: http://localhost:9090

#### Available Metrics
- **System Metrics**: CPU, memory, disk usage
- **Flask Application Metrics**:
  - Request latency and histogram
  - Request count by endpoint and method
  - HTTP status codes distribution
  - Custom business metrics
  - RabbitMQ message processing metrics

- **Django Application Metrics**:
  - Database query performance and counts
  - API endpoint usage and response times
  - Model operation counts (creates, updates, deletes)
  - Request processing time by view
  - Django admin action metrics

#### Dashboard Templates
Pre-configured dashboards include:
- Microservices Overview
- Service Health Status
- Database Performance
- API Performance Metrics
- RabbitMQ Queue Metrics
- Error Rate and Exception Tracking
- Service Resource Usage

#### Integration with Services
Both microservices expose Prometheus metrics:
- Main service: Metrics exposed via `prometheus-flask-exporter` at `/metrics`
- Admin service: Metrics exposed via `django-prometheus` at `/metrics`

The Prometheus server scrapes these endpoints at the configured intervals and stores the time-series data, which Grafana then visualizes through customizable dashboards.

### OpenTelemetry
The admin service is instrumented with OpenTelemetry for distributed tracing. This complements the Prometheus metrics by providing request-level tracing data that shows the journey of requests through different components of the system.

### Health Checks
- Main service: `/flask/api/health`
- Admin service: `/api/health`

## Message Queue Architecture

Both services communicate through RabbitMQ using the following message routing:

1. **Main Service:**
   - Publishes to `admin` queue when a product is liked (with `product_liked` content-type)
   - Consumes from `main` queue for product create/update/delete events

2. **Admin Service:**
   - Publishes to `main` queue when products are created/updated/deleted
   - Consumes from `admin` queue for product like events

This architecture implements the Event-Driven Communication pattern, allowing services to operate independently while maintaining data consistency.

### RabbitMQ Implementation

The project uses RabbitMQ as a message broker to enable asynchronous communication between microservices. RabbitMQ provides reliable message delivery, fault tolerance, and decoupling between services.

#### Service Provider

The project uses CloudAMQP, a fully managed RabbitMQ service that provides:
- High availability and clustering
- Secure AMQPS connections (TLS/SSL)
- Web-based management interface
- Message persistence
- Performance monitoring

#### Integration Technology

- **Client Library**: Pika 1.1.0+ (Python RabbitMQ client)
- **Protocol**: AMQP 0-9-1
- **Connection Type**: AMQPS (secure)
- **Serialization Format**: JSON

### Message Flow

The system implements a bidirectional message flow between services:

1. **Product Creation Flow**:
   - Admin service creates a product in its database
   - Admin service publishes a `product_created` message to the `main` queue
   - Main service consumes the message and creates a corresponding product record
   - No acknowledgment is required (fire-and-forget pattern)

2. **Product Update Flow**:
   - Admin service updates a product in its database
   - Admin service publishes a `product_updated` message to the `main` queue
   - Main service consumes the message and updates its product record
   - No acknowledgment is required

3. **Product Deletion Flow**:
   - Admin service deletes a product from its database
   - Admin service publishes a `product_deleted` message to the `main` queue
   - Main service consumes the message and deletes its product record
   - No acknowledgment is required

4. **Product Like Flow**:
   - Main service records a product like in its database
   - Main service publishes a message to the `admin` queue
   - Admin service consumes the message and increments the product's like count
   - No acknowledgment is required

### Queue Configuration

The RabbitMQ implementation uses the following configuration:

1. **Queues**:
   - `main`: Receives messages from the Admin service
   - `admin`: Receives messages from the Main service

2. **Message Properties**:
   - `content_type`: Used to identify message type (e.g., `product_created`, `product_updated`, `product_deleted`, `product_liked`)
   - Messages are serialized as JSON strings

3. **Consumer Configuration**:
   - `auto_ack=True`: Automatic acknowledgment of messages
   - Single-threaded consumers
   - No prefetch limit configured

4. **Producer Configuration**:
   - Direct publishing to queues (no exchanges used)
   - Connection creation and closing for each publish operation
   - No persistent messages or publisher confirms

### Queue Error Handling

The system implements several error handling strategies for RabbitMQ:

1. **Connection Error Handling**:
   - Producers catch connection exceptions and log errors
   - Producers ensure connections are closed in finally blocks
   - Consumers would need to be restarted if connections fail

2. **Message Processing Errors**:
   - Consumers use try/catch blocks around database operations
   - Failed message processing is logged but not retried (at-most-once delivery)

3. **Deployment Considerations**:
   - Consumer services run in separate Docker containers
   - Service restarts are handled by the container orchestration system
   - Containers have health checks to ensure service availability

### RabbitMQ Best Practices

The implementation follows several RabbitMQ best practices:

1. **Connection Management**:
   - Each producer creates a new connection for publishing
   - Consumers maintain long-lived connections
   - Connections are explicitly closed after use
   - Connection parameters are centralized

2. **Message Format**:
   - Consistent JSON serialization across services
   - Content-type headers for message identification
   - Simple message structures with minimal payload

3. **Security**:
   - AMQPS protocol for encrypted communication
   - Credentials managed through environment variables
   - CloudAMQP provides TLS/SSL termination

4. **Monitoring & Observability**:
   - Console logging for message receipt and processing
   - Error handling with detailed logging
   - CloudAMQP dashboard for queue monitoring

### Implementation Details

#### Main Service Producer

```python
def publish(method, body):
    params = pika.URLParameters('amqps://user:password@host/vhost')

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        properties = pika.BasicProperties(method)
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
```

#### Admin Service Consumer

```python
def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')

channel.basic_consume(queue='admin',
                     on_message_callback=callback,
                     auto_ack=True)
```

### Scaling Considerations

1. **Horizontal Scaling**:
   - Consumer containers can be scaled independently
   - CloudAMQP cluster supports high throughput
   - Message persistence ensures reliability during scaling events

2. **High Availability**:
   - CloudAMQP provides redundant message brokers
   - Messages are stored until consumed (even if consumers are down)
   - Automatic failover capabilities

3. **Future Enhancements**:
   - Implement dead-letter queues for failed messages
   - Add message TTL (Time-To-Live) for stale messages
   - Implement publisher confirms for critical messages
   - Add message batching for higher throughput

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

4. **Frontend Issues**
   - Check API endpoint configuration in `src/constant.tsx`
   - Verify CORS headers are properly set on backend services
   - Inspect browser console for JavaScript errors
   - Ensure Nginx configuration is properly routing requests
   - Check network tab for failed API requests
   - Verify that the correct environment variables are set
   - For build issues, check Node.js version compatibility
   - For styling issues, verify Bootstrap CSS is properly loaded

5. **Monitoring Stack Issues**
   - Verify Prometheus can reach service endpoints
   - Check Prometheus targets page for scraping errors
   - Ensure Grafana can connect to Prometheus data source
   - Restart monitoring services if dashboards are not populating

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines for Python code
   - Follow ESLint/Prettier rules for JavaScript/TypeScript
   - Use type hints in Python and TypeScript
   - Write docstrings for all functions and classes

2. **Testing**
   - Write unit tests for new features
   - Maintain test coverage above 80%
   - Run tests before committing
   - Use Jest for frontend testing
   - Use pytest for backend testing

3. **Documentation**
   - Update API documentation when making changes
   - Document new environment variables
   - Keep README up to date
   - Document component props in frontend code
   - Include JSDoc comments for frontend functions

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

## License

This project is licensed under the MIT License - see the LICENSE file for details. -->

## Support

For support or questions, please contact:
- Louis Binah <louisbinah@gmail.com>
- Open an issue on the repository
