from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .models import TextModel
from utils import chunk_text, embed_chunked_text

router = APIRouter(prefix="/chunk-and-embed", tags=["chunk-and-embed"])


@router.post("", include_in_schema=False)
@router.post("/")
async def chunk_and_embed(text_model: TextModel):
    try:
        text = text_model.text
        threshold = text_model.chunk_threshold
        chunked_text = chunk_text(text, threshold)
        chunked_and_embedded_text = embed_chunked_text(chunked_text)

        return JSONResponse({"data": chunked_and_embedded_text})
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc
