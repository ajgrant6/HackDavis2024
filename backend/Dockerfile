# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir gunicorn
# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the Flask app runs
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the Flask app
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]