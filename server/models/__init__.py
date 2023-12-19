from db.database import SessionLocal
db = SessionLocal()

def insert(self) -> None:
    db.session.add(self)
    db.session.commit()

def update() -> None:
    db.session.commit()

def delete(self) -> None:
    db.session.delete(self)
    db.session.commit()

def rollback() -> None:
    db.session.rollback()