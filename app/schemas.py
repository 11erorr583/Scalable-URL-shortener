from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


# step1: URLcreate contains data fields -- get by user
class URLCreate(BaseModel):
    original_url: HttpUrl = Field(
        ..., description="This is required Field. the original URL that will be shorten"
    )
    expiry_date: Optional[datetime] = Field(
        default=None,
        description=""" optional expiry date for shorturl formate: YY-MM-DD HH:MM:SS""",
    )
    short_code: Optional[str] = Field(
        default=None,
        max_length=20,
        min_length=3,
        description="users can choose custom short string",
    )


# step:2 URLResponse have data fields that are generated after API response
class URLResponse(BaseModel):
    # allows reading data from ORM attributes
    model_config = {"from_attributes": True}
    created_at: datetime = Field(
        ...,
        description="""timestamp when short url was created""",
    )
    expiry_date: Optional[datetime] = Field(
        default=None, description="The time at which short link will be expired"
    )
    original_url: HttpUrl = Field(
        ..., description="the original long URL entered by user"
    )
    short_code: str = Field(
        ..., description="The short code that will be the part of shortened url"
    )
    id: int = Field(..., description="This is the unique id for shortened URL")
    short_url: str = Field(..., description=" final new short url generated")


# step3: creating TrackingResponse schema
class TrackingResponse(BaseModel):
    model_config = {"from_attributes": True}
    timestamp: datetime = Field(
        ..., description="Time at which user clicks the short urls"
    )
    masked_ip_address: str = Field(
        ..., description="This is ip address of the request machine masked for security"
    )
    user_agent_os: str = Field(..., description="The os of user agent")
    user_agent_browser: str = Field(..., description="the browser of user_agent")
    referrer_url: Optional[str] = Field(
        None, description=" the URL of referrer from where the traffic came"
    )
    id: int = Field(
        ..., description="The unique id for every click event recorded on shortURL"
    )
    url_id: int = Field(..., description="The identifier for url which is shortened")
