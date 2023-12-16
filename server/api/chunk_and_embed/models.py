from pydantic import BaseModel


class TextModel(BaseModel):
    text: str
    chunk_threshold: int | None = 1024

