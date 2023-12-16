import requests
import gzip
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .models import ChatPdfModel
from utils import (
    chunk_text,
    embed_chunked_text,
    extract_text_from_pdf_content,
    parallel_compress,
)
from pympler.asizeof import asizeof

router = APIRouter(prefix="/chatpdf", tags=["chatpdf"])


@router.post("", include_in_schema=False)
@router.post("/upload")
async def upload(chatpdf_model: ChatPdfModel):
    try:
        url = chatpdf_model.url
        response = requests.get(url)
        pdf_content = response.content
        pdf_text_list = extract_text_from_pdf_content(response.content)
        size_in_mb = asizeof(pdf_content) / (1024.0**2)
        if size_in_mb > 5:
            compressed_content = gzip.compress(pdf_content)
        else:
            compressed_content = parallel_compress(pdf_content)

        chunk_threshold = 10
        chunked_pdf_data = []
        for text in pdf_text_list:
            chunked_text = chunk_text(text, chunk_threshold)
            chunked_and_embedded_text = embed_chunked_text(chunked_text)
            for chunk in chunked_and_embedded_text:
                print(chunk)
                break
            break

        return JSONResponse(
            {
                "text": pdf_text_list,
                # "bytes": f"{pdf_content}",
                # "compressed": f"{compressed_content}",
            }
        )
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc
