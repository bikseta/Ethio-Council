from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import admin_hierarchy, auth, churches, denominations, diaspora, leaders, ministries

app = FastAPI(title="ECFE Core Platform Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(churches.router, prefix="/api/v1/churches", tags=["churches"])
app.include_router(denominations.router, prefix="/api/v1/denominations", tags=["denominations"])
app.include_router(ministries.router, prefix="/api/v1/ministries", tags=["ministries"])
app.include_router(leaders.router, prefix="/api/v1/leaders", tags=["leaders"])
app.include_router(admin_hierarchy.router, prefix="/api/v1/hierarchy", tags=["hierarchy"])
app.include_router(diaspora.router, prefix="/api/v1/diaspora", tags=["diaspora"])


@app.get("/")
def root():
    return {
        "service": "core-platform-service",
        "routers": ["auth", "churches", "ministries", "denominations", "leaders", "hierarchy", "diaspora"],
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "core-platform-service"}
