from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import admin_hierarchy, auth, churches, denominations, diaspora, leaders, ministries


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ethio-Council Core Platform API",
    description="ECFE national digital platform core APIs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(churches.router)
app.include_router(denominations.router)
app.include_router(ministries.router)
app.include_router(leaders.router)
app.include_router(admin_hierarchy.router)
app.include_router(diaspora.router)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "core-platform-service"}


@app.get("/")
def root():
    return {"message": "Ethio-Council core platform service", "docs": "/docs"}
