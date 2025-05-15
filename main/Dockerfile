FROM python:alpine

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /home/app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Upgrade pip
RUN pip install --upgrade pip
# Copy requirements and install Python packages
COPY --chown=appuser:appgroup ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files and give ownership to non-root user
COPY --chown=appuser:appgroup . /home/app


# Change to non-root user
USER appuser

EXPOSE 5000
ENV FLASK_APP=main.py

# Define commands directly with conditional migration initialization
ENTRYPOINT ["sh", "-c", "if [ ! -d 'migrations' ]; then flask db init; else echo 'Migrations directory exists, skipping init'; fi && flask db migrate -m 'Auto migration' && flask db upgrade && python main.py"]