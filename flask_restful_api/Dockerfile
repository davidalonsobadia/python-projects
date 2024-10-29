# Use the official Python image with version 3.10 as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port your Flask app is listening on
EXPOSE 5000

# Set the environment variable to indicate production mode
ENV FLASK_ENV=production

RUN chmod +x ./start.sh

# Set the entrypoint command to run the Flask app using Gunicorn
CMD ["./start.sh"]
