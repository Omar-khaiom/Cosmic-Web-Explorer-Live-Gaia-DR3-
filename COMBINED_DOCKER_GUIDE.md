# Combined Docker Container Guide

## Overview

`Dockerfile.app` creates a single container that runs:
- **FastAPI Backend** (port 5000 internally)
- **Nginx Reverse Proxy** (port 8080 externally)
- **Static Frontend** (served via Nginx)

Everything is accessible on **port 8080**.

## Quick Start

### Build the combined image

```powershell
cd d:\space
docker build -f Dockerfile.app -t stellar-cartographer-combined:latest .
```

### Run the container

```powershell
docker run -d `
  -p 8080:8080 `
  -v d:\space\data:/app/data `
  -v d:\space\logs:/app/logs `
  --name stellar-app `
  stellar-cartographer-combined:latest
```

### Access the app

- **Frontend:** http://localhost:8080/viewer/index.html
- **Backend API:** http://localhost:8080/api/stars/region?ra=0&dec=0&radius=5
- **API Docs:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/health

### View logs

```powershell
docker logs -f stellar-app
```

### Stop the container

```powershell
docker stop stellar-app
docker rm stellar-app
```

## Docker Compose (Combined)

Create a simplified `docker-compose.yml` for single container deployment:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.app
    container_name: stellar-cartographer-app
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

networks:
  default:
    name: stellar-network
```

Run with:
```powershell
docker-compose -f docker-compose-combined.yml up -d --build
```

## Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Container (8080)             │
├─────────────────────────────────────────────┤
│  Nginx Reverse Proxy (Supervisor managed)   │
│  ├─ Static Frontend: /viewer/               │
│  ├─ /api/* → Backend (5000)                 │
│  └─ /docs, /health → Backend (5000)         │
├─────────────────────────────────────────────┤
│  FastAPI Uvicorn (Supervisor managed)       │
│  └─ Backend API (localhost:5000)            │
└─────────────────────────────────────────────┘
```

## Push to Docker Hub

```powershell
docker tag stellar-cartographer-combined:latest omarkhaiom/stellar-cartographer:latest
docker login
docker push omarkhaiom/stellar-cartographer:latest
```

Then deploy with:
```powershell
docker run -d -p 8080:8080 omarkhaiom/stellar-cartographer:latest
```

## Advantages

✅ **Single container** - Easy to manage and deploy  
✅ **One port** - No port conflicts  
✅ **Nginx reverse proxy** - Production-grade load balancing  
✅ **Supervisor** - Automatic service management & restart  
✅ **Health checks** - Container monitoring  
✅ **Volume persistence** - Data survives container restarts  

## Troubleshooting

**Container exits immediately:**
```powershell
docker logs stellar-app
```

**Port 8080 already in use:**
```powershell
docker run -d -p 9000:8080 stellar-cartographer-combined:latest
# Access at http://localhost:9000
```

**Rebuild without cache:**
```powershell
docker build -f Dockerfile.app --no-cache -t stellar-cartographer-combined:latest .
```

**Check running services inside container:**
```powershell
docker exec stellar-app ps aux
```

**Access container shell:**
```powershell
docker exec -it stellar-app bash
```
