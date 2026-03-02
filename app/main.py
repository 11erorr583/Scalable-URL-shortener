from fastapi import FastAPI
from app.routers import url, analytics
from slowapi.errors import RateLimitExceeded
from app.database import database_engine, Base
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.utils.limiter import limiter

app = FastAPI(
    title="URL shortner",
    description=" A simple API shortner with analytics tracking",
    servers=[{"url": "http://127.0.0.1:8000", "description": "Local server"}],
)
# --> to solve CROS I added CORSMiddleware allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# creating database table
Base.metadata.create_all(bind=database_engine)

# include url and analytics router
app.include_router(url.router)
app.include_router(analytics.router)


# root
@app.get("/")
def root():
    return {"message": "URL shortner API is running"}
