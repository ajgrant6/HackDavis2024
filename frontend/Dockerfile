# Stage 1: Build the React app
FROM node:18 AS build
WORKDIR /app

# Copy package.json and package-lock.json
COPY job-scoper/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY job-scoper/ ./

# Build the React app
RUN npm run build

# Stage 2: Serve the React app with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port on which the app will run
EXPOSE 80

# Command to start Nginx server
CMD ["nginx", "-g", "daemon off;"]
