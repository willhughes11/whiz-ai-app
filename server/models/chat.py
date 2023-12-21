from sqlalchemy import Column, String, TIMESTAMP, JSON
from db.database import Base
from datetime import datetime
from sqlalchemy.orm import Session
from . import update, insert


class Chat(Base):
    __tablename__ = "chat"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    history = Column(JSON, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now)

    def response(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "history": self.history,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def get_chat_by_id(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    return chat.response()


def update_chat(db: Session, chat_id: int, title: str = None, history: dict = None):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    chat.history = history if history is not None else chat.history
    chat.title = title if title is not None else chat.title
    update(chat)

    return chat.response()


def add_chat(db: Session, chat_id: str, title: str, history: dict):
    chat = Chat(id=chat_id, title=title, history=history)
    insert(chat)
    return chat.response()
