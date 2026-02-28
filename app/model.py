from app.database import Base  # imports Base class
from sqlalchemy import Text, String, DateTime, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class URL(Base):
    __tablename__ = "URL"
    # primary key
    id = Column(
        Integer,
        primary_key=True,
    )

    # original logn URL
    original_url = Column(Text)

    # code for short_URL, indexed for fast retrieval
    short_code = Column(String(20), index=True)

    # expiration_date
    expiry_date = Column(DateTime, nullable=True)

    # creation_date
    created_at = Column(DateTime)

    # relationship -- one to many
    tracking = relationship("Tracking", back_populates="url")


class Tracking(Base):
    __tablename__ = "tracking"

    # primary_key
    id = Column(Integer, primary_key=True)

    # datatype used Text as we do not store original ip address
    masked_ip_address = Column(Text)

    # URL_id foreign key-=> the primary key of URL model (id), indexed for direct access
    url_id = Column(Integer, ForeignKey("URL.id"), index=True)

    # user agent browser
    user_agent_browser = Column(String)

    # user agent operating system
    user_agent_os = Column(String)

    # Referrer URL -> Where the traffic came from
    referrer_url = Column(Text)

    # TimeStamp -> of the click
    timestamp = Column(DateTime)

    # relationship: one URL can have many trcking instances (one to many relationship)
    url = relationship("URL", back_populates="tracking")
