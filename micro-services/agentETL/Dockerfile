# Use a base image with Python and cron
FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /app

# Copy your ETL scripts into the container
COPY src/etls/ /app/src/

# Install dependencies
COPY micro-services/agentETL/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set up the cron job by creating a crontab file
COPY micro-services/agentETL/crontab /etc/cron.d/etl-cron

# Make the crontab file executable
RUN chmod 0644 /etc/cron.d/etl-cron

# Apply the cron job
RUN crontab /etc/cron.d/etl-cron

# Create a log file for cron output
RUN touch /var/log/cron.log

# Run the cron daemon in the foreground
CMD cron && tail -f /var/log/cron.log
