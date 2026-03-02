from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv
import os

from app.database import get_db
from app.model import URL
from app.schemas import URLCreate, URLResponse
from app.utils.helpers import generate_short_code, save_tracking
from app.utils.limiter import limiter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# loading one global BASE_URL from .enc
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

router = APIRouter(tags=["URLS"])


@router.post("/shorten", status_code=201, response_model=URLResponse)
@limiter.limit("10/minute")
def shorten_url(request: Request, url_data: URLCreate, db: Session = Depends(get_db)):
    # \ check if the custom code already is in database
    if url_data.short_code:
        code = url_data.short_code
    else:
        code = generate_short_code()

    # now checking if any url record with this code existed
    record = db.query(URL).filter(URL.short_code == code).first()
    if record:
        raise HTTPException(status_code=400, detail="short code already taken")
    create_at = datetime.now()
    # creating object from URL model
    new_url = URL(
        original_url=str(url_data.original_url),
        short_code=code,
        short_url=f"{BASE_URL}/{code}",
        expiry_date=url_data.expiry_date,
        created_at=create_at,
    )

    # adding new record into the database
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    # now build the full short url
    return new_url


# now writing the get requests
@router.get("/{short_code}", tags=["redirect"])
@limiter.limit("10/minute")
def redirect_to_url(
    request: Request,
    short_code: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # check if short_code in database
    search_code = db.query(URL).filter(URL.short_code == short_code).first()
    if not search_code:
        raise HTTPException(status_code=404, detail="page not found")
    if search_code.expiry_date and search_code.expiry_date < datetime.now():
        raise HTTPException(status_code=410, detail=" short url expired ")

    background_tasks.add_task(save_tracking, search_code.id, request)
    response = RedirectResponse(url=search_code.original_url, status_code=302)
    response.headers["Access-Control-Allow-Origin"] = (
        "*"  # --> to solve CORS error I try to manually add CORS header for all origins
    )
    return response


# last part: delete record --> shortcut code
@router.delete("/{short_code}", tags=["DELETE"])
@limiter.limit("10/minute")
def delete_short_code(short_code: str, request: Request, db: Session = Depends(get_db)):
    # search for a short_code first
    check = db.query(URL).filter(URL.short_code == short_code).first()
    if not check:
        raise HTTPException(status_code=404, detail=f"{short_code} does not exist")
    else:
        db.delete(check)
        db.commit()
        return {"message": f"{short_code} deleted successfully"}
