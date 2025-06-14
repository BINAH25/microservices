FROM python:alpine

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /home/app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip
# Copy requirements and install Python packages
COPY --chown=appuser:appgroup ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files and give ownership to non-root user
COPY --chown=appuser:appgroup . /home/app

# Copy and set permissions for entrypoint
COPY --chown=appuser:appgroup ./entrypoint.sh /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh


# Change to non-root user
USER appuser

EXPOSE 8000

CMD ["/home/app/entrypoint.sh"]