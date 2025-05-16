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
# Copy entrypoint script
COPY ./start.sh /home/app/start.sh

# Give execute permissions to entrypoint script
RUN chmod +x /home/app/start.sh


EXPOSE 5000
ENV FLASK_APP=main.py

# ENTRYPOINT using root, with migration logic
CMD ["/home/app/start.sh"]
