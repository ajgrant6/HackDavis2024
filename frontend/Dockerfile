# Use an official Node.js image as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY job-scoper/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY job-scoper/ ./

# Build the React app
RUN npm run build

# Install a simple HTTP server to serve the static files
RUN npm install -g serve

# Expose the port on which the app will run
EXPOSE 3000

# Command to serve the app
CMD ["serve", "-s", "build", "-l", "3000"]