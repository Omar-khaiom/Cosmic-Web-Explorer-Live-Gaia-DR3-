# Multi-service container: Nginx reverse proxy + FastAPI backend
FROM python:3.11-slim

WORKDIR /app

# Install Nginx and supervisor
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend_code/

# Copy frontend files
COPY viewer/ /app/viewer/
COPY data/ /app/data/

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create supervisor configuration
RUN mkdir -p /etc/supervisor/conf.d
COPY <<EOF /etc/supervisor/conf.d/services.conf
[supervisord]
nodaemon=true
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:uvicorn]
directory=/app/backend_code
command=uvicorn app:app --host 127.0.0.1 --port 5000
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/uvicorn.err.log
stdout_logfile=/var/log/supervisor/uvicorn.out.log

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/nginx.err.log
stdout_logfile=/var/log/supervisor/nginx.out.log
EOF

# Expose port 8080 (Nginx listening)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/_health || exit 1

# Run supervisor to manage both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/services.conf"]
