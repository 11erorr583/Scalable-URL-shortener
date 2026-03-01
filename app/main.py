from fastapi import FastAPI, Request
from app.routers import url, analytics
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import database_engine, Base
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="URL shortner", description=" A simple API shortner with analytics tracking"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting up rate limiter
limiter = Limiter(key_func=get_remote_address)
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
