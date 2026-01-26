# Build stage for Node.js (Tailwind CSS)
FROM node:20-alpine AS node-builder

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy static files and build CSS
COPY static/ ./static/
RUN npx @tailwindcss/cli -i static/css/styles.css -o static/css/dist/styles.css --minify


# Production stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy built CSS from node stage
COPY --from=node-builder /app/static/css/dist/ ./static/css/dist/

# Collect static files
RUN python manage.py collectstatic --no-input

# Create media directory
RUN mkdir -p /app/media

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
