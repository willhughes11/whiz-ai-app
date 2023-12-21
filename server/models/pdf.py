from sqlalchemy import Column, String, Integer, TIMESTAMP, BLOB
from db.database import Base
from datetime import datetime
from sqlalchemy.orm import Session
from . import insert


class Pdf(Base):
    __tablename__ = "pdf"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    pdf = Column(BLOB, index=True, nullable=False)
    num_pages = Column(Integer, nullable=False)
    compression_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def response(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "pdf": self.pdf,
            "num_pages": self.num_pages,
            "compression_type": self.compression_type,
            "created_at": self.created_at,
        }


def get_pdf_by_id(db: Session, pdf_id: int):
    pdf = db.query(Pdf).filter(Pdf.id == pdf_id).first()
    return pdf.response()


def add_pdf(db: Session, pdf_id: str, title: str, pdf: bytes, num_pages: int, compression_type: str):
    pdf = Pdf(id=pdf_id, title=title, pdf=pdf, num_pages=num_pages, compression_type=compression_type)
    insert(pdf)
    return pdf.response()
