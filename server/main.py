from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat
from api.chatpdf import router as chatpdf
from api.chunk_and_embed import router as chunk_and_embed

from models import pdf
from db.database import SessionLocal, engine
pdf.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(chatpdf.router)
app.include_router(chunk_and_embed.router)