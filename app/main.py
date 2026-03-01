from fastapi import FastAPI
from app.routers import url, analytics
from app.database import database_engine, Base

app = FastAPI(
    title="URL shortner", description=" A simple API shortner with analytics tracking"
)

# creating database table
Base.metadata.create_all(bind=database_engine)

# include url and analytics router
app.include_router(url.router)
app.include_router(analytics.router)


# root
@app.get("/")
def root():
    return {"message": "URL shortner API is running"}
