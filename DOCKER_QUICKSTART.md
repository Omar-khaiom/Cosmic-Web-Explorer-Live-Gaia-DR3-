# Docker Quickstart Guide

## Prerequisites

- **Docker Desktop** installed on Windows
- PowerShell 5+ or Command Prompt

## Quick Start (Recommended)

Run both services with Docker Compose:

```powershell
cd d:\space
docker-compose up --build
```

**Expected Output:**
```
celestial-navigator-backend  | INFO:     Uvicorn running on http://0.0.0.0:5000
celestial-navigator-frontend | Serving HTTP on 0.0.0.0 port 3000
```

**Access the app:**
- Frontend: http://localhost:3000/viewer/index.html
- Backend API: http://localhost:5000/docs
- Health check: http://localhost:5000/health

## Useful Docker Commands

### Start services in background
```powershell
docker-compose up -d --build
```

### View logs
```powershell
docker-compose logs -f          # All services
docker-compose logs -f backend  # Backend only
docker-compose logs -f frontend # Frontend only
```

### Stop services
```powershell
docker-compose down
```

### Remove containers and images
```powershell
docker-compose down -v  # Remove volumes too
docker rmi celestial-navigator-backend celestial-navigator-frontend
```

### Rebuild images
```powershell
docker-compose build --no-cache
```

### Execute command in running container
```powershell
docker-compose exec backend bash
docker-compose exec frontend bash
```

## Build Individual Images

### Backend only
```powershell
docker build -f Dockerfile.backend -t celestial-navigator-backend:latest .
docker run -p 5000:5000 -v d:\space\data:/app/data -v d:\space\logs:/app/logs celestial-navigator-backend:latest
```

### Frontend only
```powershell
docker build -f Dockerfile.frontend -t celestial-navigator-frontend:latest .
docker run -p 3000:3000 celestial-navigator-frontend:latest
```

## Push to Docker Hub

```powershell
# Tag images (replace 'omarkhaiom' with your Docker Hub username)
docker tag celestial-navigator-backend:latest omarkhaiom/stellar-cartographer-backend:latest
docker tag celestial-navigator-frontend:latest omarkhaiom/stellar-cartographer-frontend:latest

# Login and push
docker login
docker push omarkhaiom/stellar-cartographer-backend:latest
docker push omarkhaiom/stellar-cartographer-frontend:latest
```

## Troubleshooting

**Port 5000 or 3000 already in use:**
```powershell
# Change ports in docker-compose.yml:
# ports: ["5001:5000"]  # Maps container 5000 to host 5001
docker-compose down
docker-compose up -d --build
```

**Container won't start:**
```powershell
docker-compose logs backend  # Check error messages
docker-compose logs frontend
```

**Stuck containers:**
```powershell
docker-compose down --remove-orphans
docker-compose up -d --build
```

**Clear everything and restart fresh:**
```powershell
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## Notes

- Data volumes persist at `./data` and `./logs` (auto-synced from host)
- Health checks ensure services are ready before accepting traffic
- Services restart automatically if they crash (`restart: unless-stopped`)
- Both services are on the same Docker network (`celestial-network`) for easy inter-service communication
