# Use Python Slim base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the app code
COPY . .

# Set environment variables
ENV FLASK_APP=app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service port
EXPOSE 5001

# Command to run the app with migration logic
CMD ["sh", "-c", "\
    if [ ! -d 'migrations' ]; then \
        flask db init && \
        flask db migrate -m 'Initial migration' && \
        flask db upgrade; \
    else \
        flask db migrate -m 'Update models' && \
        flask db upgrade; \
    fi && \
    flask run --host=0.0.0.0 --port=5001"]