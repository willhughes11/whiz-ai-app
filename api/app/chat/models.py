from pydantic import BaseModel


class Conversation(BaseModel):
    history: list[dict]
    model: str
