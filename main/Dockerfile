FROM python:alpine

WORKDIR /home/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /home/app

EXPOSE 5000
ENV FLASK_APP=main.py

# ENTRYPOINT using root, with migration logic
ENTRYPOINT ["sh", "-c", "\
  if [ ! -d 'migrations' ]; then \
    flask db init; \
  else \
    echo 'Migrations directory exists, skipping init'; \
  fi && \
  flask db migrate -m 'Auto migration' && \
  flask db upgrade && \
  python main.py"]
