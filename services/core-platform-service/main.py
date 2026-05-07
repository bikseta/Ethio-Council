from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import auth_router, members, churches, reports, admin

app = FastAPI(
    title="Ethio-Council Core Platform API",
    description="National Digital Platform for the Evangelical Churches Fellowship of Ethiopia (ECFE)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(members.router, prefix="/api/v1/members", tags=["Members"])
app.include_router(churches.router, prefix="/api/v1/churches", tags=["Churches"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Administration"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "core-platform-service", "version": "1.0.0"}

@app.get("/")
def root():
    return {"message": "Ethio-Council ECFE Digital Platform Core API", "docs": "/docs"}
