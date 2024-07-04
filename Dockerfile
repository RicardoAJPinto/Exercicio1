FROM python:3.9.16-slim

# Create directory for backups
RUN mkdir -p /mnt/backups/

# Set the working directory
WORKDIR /

# Copy all files into the container
COPY . .

# Install cron and any other necessary packages
RUN apt-get update && apt-get install -y cron 

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the crontab file into the appropriate location
COPY crontab /etc/cron.d/crontab

# Ensure the crontab file has the correct permissions
RUN chmod 0644 /etc/cron.d/crontab

# Ensure the script to be run by cron has the correct permissions
RUN chmod +x backup.py

# Apply the crontab file
RUN crontab /etc/cron.d/crontab


RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log