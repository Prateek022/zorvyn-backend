from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from app.database import engine, Base
from app.routers import auth, users, records, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zorvyn Finance Backend",
    description="Finance Data Processing and Access Control Backend API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Health"])
@limiter.limit("60/minute")
def root(request: Request):
    return {
        "status": "running",
        "message": "Zorvyn Finance Backend API is live",
        "docs": "/docs"
    }