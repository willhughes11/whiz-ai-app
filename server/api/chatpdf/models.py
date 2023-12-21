from pydantic import BaseModel


class ChatPdfModel(BaseModel):
    id: str | None
    history: list[dict] | None
    model: str | None


class ChatPdfUploadModel(BaseModel):
    url: str | None
