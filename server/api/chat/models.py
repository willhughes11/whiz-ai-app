from pydantic import BaseModel


class ChatModel(BaseModel):
    history: list[dict]
    model: str
