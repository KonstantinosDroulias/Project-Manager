# Stage 1: Build
FROM python:3.13-slim AS builder

WORKDIR /app

# Install System Deps & Node
RUN apt-get update && apt-get install -y nodejs npm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python Deps
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node Deps
COPY package.json package-lock.json* ./
RUN npm install

# COPY PROJECT FILES (This puts your real static files in)
COPY . .

# Build Tailwind (Real build on real files)
RUN npm run build

# Stage 2: Production
FROM python:3.13-slim

RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app
WORKDIR /app

# Copy Python Environment
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy App Code
COPY --chown=appuser:appuser . .

# Copy Built Assets (Overwrite static with the built version)
COPY --from=builder --chown=appuser:appuser /app/static /app/static

USER appuser
EXPOSE 8000
RUN chmod +x /app/entrypoint.prod.sh
CMD ["/app/entrypoint.prod.sh"]