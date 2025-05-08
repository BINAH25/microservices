FROM python:alpine

WORKDIR /home/app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
# Upgrade pip
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /home/app

EXPOSE 5000
ENV FLASK_APP=main.py

# Define commands directly with conditional migration initialization
ENTRYPOINT ["sh", "-c", "if [ ! -d 'migrations' ]; then flask db init; else echo 'Migrations directory exists, skipping init'; fi && flask db migrate -m 'Auto migration' && flask db upgrade && python main.py"]