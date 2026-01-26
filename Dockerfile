# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- NEW: Install System Deps & Node.js (for Tailwind) ---
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# ---------------------------------------------------------

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW: Build Tailwind CSS ---
# 1. Copy package.json (assuming it exists)
COPY package.json package-lock.json* /app/
# 2. Install Node dependencies
RUN npm install
# 3. Copy the entire project (Tailwind needs to scan your templates!)
COPY . .
# 4. Build the CSS
RUN npm run watch:css
# -------------------------------

# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code (This copies your source code)
COPY --chown=appuser:appuser . .

# --- NEW: Copy the BUILT Static files (CSS) from builder ---
# This overwrites the local static folder with the one containing your built CSS
COPY --from=builder --chown=appuser:appuser /app/static /app/static
# -----------------------------------------------------------

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Make entry file executable
RUN chmod +x /app/entrypoint.prod.sh

# Start the application
CMD ["/app/entrypoint.prod.sh"]