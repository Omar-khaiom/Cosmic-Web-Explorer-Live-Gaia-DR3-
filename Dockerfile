# Simple combined container: reuse existing image with all deps
# We base on omarkhaiom/celestial-navigator:latest (already has Python + libs)

FROM omarkhaiom/celestial-navigator:latest

# Work dir must remain the backend folder so "python -m uvicorn app:app" still works
WORKDIR /app/backend

# Overlay updated backend, viewer, and data onto the existing image
COPY backend/ /app/backend/
COPY viewer/ /app/viewer/
COPY data/ /app/data/

# Keep the base image's CMD/entrypoint (it already starts the app)
