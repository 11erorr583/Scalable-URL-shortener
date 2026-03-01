from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import URL, Tracking
from app.schemas import TrackingResponse

router = APIRouter(tags=["Analytics"])


@router.get(
    "/Analytics/{short_code}", status_code=200, response_model=List[TrackingResponse]
)
def tracking_analytics(short_code: str, db: Session = Depends(get_db)):

    # fetch all tracking records for that record using url_id
    # get url_id from URL model using short_code
    id_url = db.query(URL).filter(URL.short_code == short_code).first()
    # if url not found raise exception
    if not id_url:
        raise HTTPException(status_code=404, detail="URL not found")
    # get tracking record using id_url
    records = db.query(Tracking).filter(Tracking.url_id == id_url.id).all()
    return records
