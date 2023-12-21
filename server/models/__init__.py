from db.database import SessionLocal

db = SessionLocal()


def insert(self) -> None:
    db.add(self)
    db.commit()


def update(self) -> None:
    db.commit()


def delete(self) -> None:
    db.delete(self)
    db.commit()


def rollback(self) -> None:
    db.rollback()
