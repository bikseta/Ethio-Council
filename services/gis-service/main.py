from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Ethio-Council GIS Service",
    description="Geographic Information System service for ECFE platform",
    version="1.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "healthy", "service": "gis-service", "version": "1.0.0"}

@app.get("/")
def root():
    return {"message": "Ethio-Council GIS Service", "docs": "/docs"}

@app.get("/api/v1/gis/churches/geojson")
def churches_geojson(denomination_id: str = None, region_id: str = None):
    """Return churches as GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": [],
        "meta": {"note": "Connect to PostGIS for real data", "denomination_id": denomination_id, "region_id": region_id},
    }

@app.get("/api/v1/gis/crisis/geojson")
def crisis_geojson(severity: str = None):
    """Return crisis reports as GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": [],
        "meta": {"note": "Connect to PostGIS for real data", "severity": severity},
    }

@app.get("/api/v1/gis/regions/geojson")
def regions_geojson():
    """Return regions as GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": [],
        "meta": {"note": "Connect to PostGIS for real data"},
    }

@app.get("/api/v1/gis/tiles/{z}/{x}/{y}")
def get_tile(z: int, x: int, y: int):
    """Placeholder for vector tile endpoint."""
    return {"z": z, "x": x, "y": y, "note": "Vector tiles not yet implemented"}
