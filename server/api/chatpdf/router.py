import uuid
import gzip
import requests
from pympler.asizeof import asizeof
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
import weaviate
from weaviate.embedded import EmbeddedOptions
from .models import ChatPdfModel
from utils import (
    extract_text_from_pdf_content,
    parallel_compress,
    extract_pdf_name,
    process_pdf,
    process_pdf_multithreaded,
)

router = APIRouter(prefix="/chatpdf", tags=["chatpdf"])


@router.post("", include_in_schema=False)
@router.post("/upload")
async def upload(chatpdf_model: ChatPdfModel):
    try:
        pdf_id = uuid.uuid4()
        url = chatpdf_model.url
        pdf_file_name = extract_pdf_name(url)
        response = requests.get(url)
        pdf_content = response.content
        pdf_text_list = extract_text_from_pdf_content(response.content)
        size_in_mb = asizeof(pdf_content) / (1024.0**2)
        if size_in_mb > 5:
            compressed_content = gzip.compress(pdf_content)
        else:
            compressed_content = parallel_compress(pdf_content)

        chunk_threshold = 25
        token_overlap = 5
        result_data = []
        if len(pdf_text_list) < 15:
            result_data = process_pdf(
                pdf_id, pdf_file_name, pdf_text_list, chunk_threshold, token_overlap
            )
        else:
            result_data = process_pdf_multithreaded(
                pdf_id, pdf_file_name, pdf_text_list, chunk_threshold, token_overlap
            )

        client = weaviate.Client(embedded_options=EmbeddedOptions())
        for data in result_data:
            client.data_object.create(data, "chatpdf")

        return JSONResponse(result_data)
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc
