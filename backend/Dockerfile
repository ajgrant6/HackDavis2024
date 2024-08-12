# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn, a production-grade WSGI server
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the Flask app runs
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
