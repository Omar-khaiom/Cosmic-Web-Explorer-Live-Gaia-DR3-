# Cosmic-Web Explorer (Live Gaia DR3)

Explore the Milky Way with real, live data from ESA Gaia DR3. This repo contains:

- Backend: FastAPI service that queries Gaia DR3 (TAP+) and returns stars for a sky region
- Frontend: Three.js viewer with planetarium mode, constellation overlays, and live star streaming

## Features

- **Live Gaia DR3 Data**: Real star positions, magnitudes, and colors from ESA's Gaia mission (~20,000 bright stars)
- **Full-Sky 3D**: Explore the entire celestial sphere with true 3D distances from Earth (0.1 to 100,000+ parsecs)
- **Constellation Overlays**: Toggle 10 major constellations with overlay patterns (Orion, Ursa Major, Cassiopeia, etc.)
- **Bright Star Labels**: Named stars visible on approach (Sirius, Betelgeuse, Vega, Polaris, Rigel, Arcturus, etc.)
- **Magnitude-Based Rendering**: Bright stars appear larger and more prominent; colors represent temperature
- **Frame Views**: Switch between Equatorial (EQ), Ecliptic (EP), and Galactic (GAL) coordinate frames with plane rings
- **Smart Caching**: First queries take 1-3s; cached repeats are 5-20ms

This is a trimmed, production-friendly setup with minimal dependencies and a simple start flow.

## Requirements

- Python 3.10+ (3.12 OK)
- Windows (PowerShell 5+), Linux, or macOS

## Quick Start (Windows PowerShell)

Run the helper script that starts both servers (backend on 5000, frontend on 3000):

```powershell
cd d:\space
./start_all.ps1
```

Open the viewer:
- http://localhost:3000/viewer/index.html

## Quick Start (Linux / macOS)

Run the shell script:

```bash
cd ~/space  # or wherever you cloned the repo
chmod +x start_all.sh
./start_all.sh
```

Open the viewer:
- http://localhost:3000/viewer/index.html

## About This Sky View

When you launch the app, you're viewing the entire celestial sphere from Earth, starting centered on the **Vernal Equinox** (RA 0°, Dec 0°) — the direction where the Sun appears on the spring equinox.

### Default View Region

| Coordinate | Value |
|------------|-------|
| **Right Ascension (RA)** | 0° (Vernal Equinox direction) |
| **Declination (Dec)** | 0° (Celestial Equator) |
| **Distance Range** | 0.1 - 100,000+ parsecs (~326 light-years to billions) |
| **Star Count** | ~20,000 (magnitude < 7.0 = naked-eye visible) |
| **Coordinate System** | Equatorial (ICRS) — IAU standard |

### Nearby Constellations & Regions

From the default RA=0°/Dec=0° starting point, nearby celestial regions include:

| Region | RA Range | Dec Range | Key Stars | Distance |
|--------|----------|-----------|-----------|----------|
| **Cassiopeia** | 2.3°-28.6° | +59° to +63° | Scheherazade (γ Cas) | ~150 ly |
| **Andromeda Galaxy (M31)** | 0.7°-2.7° | +25° to +42° | Alpheratz (α And) | 2.5 M ly |
| **Perseus** | 2°-4° | +31° to +58° | Algol (β Per) | ~93 ly |
| **Pisces** | 23°-3° | -3° to +33° | Alrescha (α Psc) | ~100 ly |
| **Cetus** | 0°-3° | -24° to +3° | Diphda (β Cet) | ~96 ly |
| **Triangulum** | 1°-3° | +25° to +35° | Mothallah (α Tri) | ~60 ly |
| **Pegasus** | 22°-0° | +7° to +35° | Markab (α Peg) | ~133 ly |

### Sky Navigation

**Keyboard & Mouse Controls:**
- **WASD** — Navigate through space
- **Mouse Drag** — Rotate view
- **Shift** — Move slower (fine control)
- **EQ/EP/GAL buttons** — Switch coordinate frames
- **Search box** — Find stars by name
- **Click a star** — Show details and navigate to it

### Famous Stars Tour (Start with any constellation)

The viewer includes guided waypoints to major bright and nearby stars:
1. **Sirius** (RA 101.3°, Dec -16.7°) — Brightest visible star, 8.6 light-years
2. **Betelgeuse** (RA 88.8°, Dec +7.4°) — Red supergiant in Orion, 430-600 light-years
3. **Alpha Centauri (Rigil)** (RA 219.9°, Dec -60.8°) — Nearest star system, 4.37 light-years
4. **Vega** (RA 279.2°, Dec +38.8°) — Brilliant blue star, 25 light-years

### Download local catalog (for ~20k bright stars)

By default, if the local SQLite catalog is missing, the API falls back to a tiny JSON sample (~20 stars). To see the full bright layer (~20,000 stars, mag < 7), download and build the local catalog once:

**Windows (PowerShell):**
```powershell
cd d:\space\backend
pip install -r requirements.txt
python scripts\download_gaia_catalog.py --mag-limit 7.0 --output d:\space\data\gaia_catalog.db
```

**Linux / macOS (Bash):**
```bash
cd ~/space/backend
pip3 install -r requirements.txt
python3 scripts/download_gaia_catalog.py --mag-limit 7.0 --output ~/space/data/gaia_catalog.db
```

Then restart the backend. If you previously hit the bright-catalog endpoint, the result may be cached; restarting clears the in-memory cache. Alternatively, call with a slightly different limit (e.g., `--mag-limit 7.01`).

**Speed tips:**
- For faster download, use `--mag-limit 6.5` (~9,000 bright stars only)
- First download takes 2-5 minutes; subsequent restarts are instant (cached)

Windows quick start (one-click)

If you prefer a double-clickable launcher, use the included `start_all.bat` from the repo root. It opens two command windows: one for the backend and one for the static frontend.

Steps:

1. Double-click `d:\space\start_all.bat` or run it from PowerShell/CMD:

cd d:\space
.\start_all.bat

2. Open http://localhost:3000/viewer/index.html

PowerShell gotcha & Troubleshooting

- "the term 'start_all.ps1' is not recognized" when typing `start_all.ps1` in PowerShell usually means one of:

  1. You're not in the repository directory. Run `cd d:\space` first.
  2. PowerShell requires `.`/`\` prefix to run local scripts: use `.\\start_all.ps1` or `./start_all.ps1`.
  3. Execution policy blocks scripts. Temporarily allow scripts for the current PowerShell session:

  Open PowerShell as Administrator or for the current session run:

  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

  Then run: `./start_all.ps1`

- If you still can't run the PowerShell script, use `start_all.bat` (double-click) or start the backend and frontend manually (see Manual start above).

If anything fails, collect the single-window output and paste the logs here and I will help troubleshoot further.

You should see “Viewing XXXX stars from Gaia DR3”. As you move, new regions will stream in. The console shows when data is cached vs live.

## Manual Start

Backend API (FastAPI + Uvicorn):

```powershell
cd d:\space\backend
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

Frontend (static server):

```powershell
cd d:\space
python -m http.server 3000
```

Open the viewer:

- http://localhost:3000/viewer/index.html

## Coordinate Systems Explained

This app uses **three complementary coordinate frames**, all centered on Earth:

### 1. **Equatorial (EQ)** — Standard Astronomy Frame
- **RA (Right Ascension)**: 0°-360° (East along the celestial equator)
- **Dec (Declination)**: -90° to +90° (North-South poles)
- **Origin**: Vernal Equinox (RA 0°, Dec 0°) — direction to Spring sunrise point
- **Use**: Standard for all star catalogs and Gaia DR3 data
- **Example**: Sirius (RA 101.3°, Dec -16.7°)

### 2. **Ecliptic (EP)** — Solar System Frame
- **Ecliptic Longitude**: 0°-360° along the Sun's apparent path
- **Ecliptic Latitude**: -90° to +90° above/below the Sun's path
- **Use**: Tracking planets, solar system objects, and seasonal changes
- **Note**: Tilted ~23.4° from celestial equator (Earth's axial tilt)

### 3. **Galactic (GAL)** — Milky Way Frame
- **Galactic Longitude**: 0°-360° around the galactic plane
- **Galactic Latitude**: -90° to +90° perpendicular to galactic disk
- **Use**: Studying the structure of our galaxy
- **Center**: Sagittarius A* (black hole at galactic center)

**Use the EQ/EP/GAL buttons to switch frames and see the plane overlay rotate!**

## API

- GET /health – Health check
- GET /api/stars/region?ra=<deg>&dec=<deg>&radius=<deg>&limit=<n>

Example:

```
http://localhost:5000/api/stars/region?ra=266.4&dec=-29.0&radius=5&limit=1000
```

Response (fields abbreviated):

```
{
  "count": 1000,
  "cached": false,
  "query_time_ms": 1450.2,
  "stars": [
    {
      "source_id": "123456789",
      "ra": 266.41, "dec": -29.00,
      "x": 123.4, "y": -56.7, "z": 234.5,
      "parallax": 0.78, "distance_pc": 1282.1,
      "magnitude": 12.3, "color_bp_rp": 0.9,
      "r": 1, "g": 0.9, "b": 0.5,
      "pm_ra": -2.1, "pm_dec": 0.7
    }
  ]
}
```

## Notes

- Data is real from ESA Gaia DR3. First-time queries take ~1–3s; cached repeats are ~5–20ms.
- If the live query fails, the viewer falls back to a small CSV sample for demo only.
- Logs are written to `d:\space\logs` and ignored by Git; the folder will be created on start.

## Troubleshooting

- Port in use: change ports in `start_all.ps1` or run uvicorn with a different `--port`.
-- CORS: backend allows http://localhost:3000 (and 8000) by default (see `backend/config.py`).
- Gaia 500 errors: transient. The service auto-retries; try again or move slightly to trigger a new region.

## Deploy to Azure (Production - Two Web Apps)

### Prerequisites
✅ Azure Education Account (~$100/month free credit)
✅ Docker Hub Account (free tier)
✅ Docker Desktop installed locally
✅ GitHub Repository

### Step 1: Build & Push Docker Images

```powershell
cd d:\space
docker login

# Build backend
docker build -f Dockerfile.backend -t omarkhaiom/stellar-cartographer-backend:latest .
docker push omarkhaiom/stellar-cartographer-backend:latest

# Build frontend
docker build -f Dockerfile.frontend -t omarkhaiom/stellar-cartographer-frontend:latest .
docker push omarkhaiom/stellar-cartographer-frontend:latest
```

**Replace `omarkhaiom` with your Docker Hub username!**

### Step 2: Create Backend Web App

1. Go to [portal.azure.com](https://portal.azure.com)
2. **Create Resource** → **Web App**
3. **Basics Tab:**
   - **Name:** `celestial-navigator` (URL: celestial-navigator.azurewebsites.net)
   - **Publish:** Docker Container
   - **OS:** Linux
   - **Region:** Central India (or nearest)
   - **Plan:** Free (F1)

4. **Container Tab:**
   - **Image Source:** Other container registries
   - **Registry server URL:** `https://index.docker.io`
   - **Image and tag:** `omarkhaiom/stellar-cartographer-backend:latest`
   - **Port:** `8080`

5. **Review + Create** → **Create**

### Step 3: Create Frontend Web App

1. **Create Resource** → **Web App** (again)
2. **Basics Tab:**
   - **Name:** `celestial-navigator-viewer` (URL: celestial-navigator-viewer.azurewebsites.net)
   - **Publish:** Docker Container
   - **OS:** Linux
   - **Region:** Central India (same as backend)
   - **Plan:** Free (F1)

3. **Container Tab:**
   - **Image Source:** Other container registries
   - **Registry server URL:** `https://index.docker.io`
   - **Image and tag:** `omarkhaiom/stellar-cartographer-frontend:latest`
   - **Port:** `3000`

4. **Review + Create** → **Create**

### Step 4: Test Deployment

**Backend API:** `https://celestial-navigator.azurewebsites.net/health`
- Should respond with JSON health status

**Frontend Viewer:** `https://celestial-navigator-viewer.azurewebsites.net/viewer/index.html`
- Should load Three.js viewer and connect to backend

### Deployment Summary

| Component | URL | Port | Image |
|-----------|-----|------|-------|
| **Backend** | https://celestial-navigator.azurewebsites.net | 8080 | `omarkhaiom/stellar-cartographer-backend:latest` |
| **Frontend** | https://celestial-navigator-viewer.azurewebsites.net | 3000 | `omarkhaiom/stellar-cartographer-frontend:latest` |
| **Cost** | Free tier (F1) | Both on free | $0 (Education credit) |
| **Data** | SQLite (in-container) | Ephemeral | Downloaded on first query |

### Troubleshooting

**Frontend shows "offline":**
- Check if `main.js` has correct backend URL: `https://celestial-navigator.azurewebsites.net`
- Verify backend is running: test `/health` endpoint
- Check browser console (F12) for CORS or fetch errors

**Backend 504 timeout:**
- Wait 2-3 minutes for initial startup
- Check Logs in Azure Portal → App → Log stream
- Verify `requirements.txt` dependencies installed

**Both apps "Stopped":**
- Go to each Web App → Top menu → **Start**
- Wait 1-2 minutes for startup

## Project Structure

```
d:\space
├─ backend/                # FastAPI app
│  ├─ app.py               # Entry point
│  ├─ config.py            # Settings (CORS, logging, Gaia)
│  ├─ requirements.txt     # Minimal deps
│  ├─ routes/
│  │  └─ stars_api.py      # /api/stars endpoints
│  └─ services/
│     ├─ gaia_service.py   # Gaia DR3 TAP+ integration
│     └─ cache_service.py  # In-memory + SQLite cache
├─ viewer/                 # Three.js viewer
│  ├─ index.html
│  ├─ main.js
│  └─ three.min.js
├─ data/
│  └─ milky_way_stars.csv  # Small fallback sample
├─ Dockerfile.backend      # Backend container
├─ Dockerfile.frontend     # Frontend container
├─ docker-compose.yml      # Local multi-container setup
├─ start_all.ps1           # Local development launcher
├─ .gitignore              # Ignores logs, cache.db, etc.
├─ .dockerignore           # Ignores files in Docker builds
└─ LICENSE
```

Enjoy exploring!

How to start (Windows PowerShell)

One-click (recommended):

Open PowerShell and run:
cd d:\space
start_all.ps1 # if this fails, use the .bat launcher below or see Troubleshooting section
Opens:
Backend: http://localhost:5000
API Docs: http://localhost:5000/docs
Viewer: http://localhost:3000/viewer/index.html
Manual start:

Backend:
cd d:\space\backend
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload
Frontend:
cd d:\space
python -m http.server 3000
Open http://localhost:3000/viewer/index.html
