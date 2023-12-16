from pydantic import BaseModel


class ChatPdfModel(BaseModel):
    history: list[dict] | None = []
    model: str | None = ""
    url: str | None