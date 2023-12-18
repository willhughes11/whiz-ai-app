from sqlalchemy import Column, String, TIMESTAMP
from db.database import Base
from datetime import datetime

class Pdf(Base):
    __tablename__ = "pdf"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    pdf = Column(String, index=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
