FROM python:alpine

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /home/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install Python packages
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files and fix ownership/permissions
COPY . /home/app
RUN chown -R appuser:appgroup /home/app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Entry command to handle migrations safely
ENTRYPOINT ["sh", "-c", "\
  flask db migrate -m 'Auto migration' && \
  flask db upgrade && \
  python main.py"]
