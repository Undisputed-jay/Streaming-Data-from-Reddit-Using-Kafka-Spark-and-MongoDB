# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy producer.py, constant.py, and requirements.txt into the container
COPY producer.py /app/producer.py
COPY constant.py /app/constant.py  
COPY requirements.txt /app/requirements.txt
COPY config/reddit.conf /app/config/reddit.conf


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV KAFKA_BROKER='kafka:9092'

# Run the producer.py file when the container starts
CMD ["python", "producer.py"]
