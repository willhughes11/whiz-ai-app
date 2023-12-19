import base64
from sqlalchemy import Column, String, TIMESTAMP, BLOB
from db.database import Base
from datetime import datetime
from sqlalchemy.orm import Session


class Pdf(Base):
    __tablename__ = "pdf"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    pdf = Column(BLOB, index=True, nullable=False)
    compression_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def response(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "pdf": self.pdf,
            "compression_type": self.compression_type,
            "created_at": self.created_at,
        }


def get_pdf_by_id(db: Session, pdf_id: int):
    db_pdf = db.query(Pdf).filter(Pdf.id == pdf_id).first()
    return db_pdf.response()


def add_pdf(db: Session, pdf_id: str, title: str, pdf: bytes, compression_type: str):
    db_pdf = Pdf(id=pdf_id, title=title, pdf=pdf, compression_type=compression_type)
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf.response()
