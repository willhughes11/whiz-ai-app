import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import weaviate
from weaviate.embedded import EmbeddedOptions
from dotenv import load_dotenv
load_dotenv()

from api.chat import router as chat
from api.chatpdf import router as chatpdf
from api.chunk_and_embed import router as chunk_and_embed
from config import VECTOR_DB_CLASS_NAME

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

openai_api_key = os.getenv("OPENAI_API_KEY")
client = weaviate.Client(
    embedded_options=EmbeddedOptions(),
    additional_headers={"X-OpenAI-Api-Key": openai_api_key},
)
class_name = VECTOR_DB_CLASS_NAME
class_definition = {
    "class": class_name,
    "vectorizer": "text2vec-openai",
}

try:
    client.schema.create_class(class_definition)
except:
    ...

app.include_router(chat.router)
app.include_router(chatpdf.router)
app.include_router(chunk_and_embed.router)