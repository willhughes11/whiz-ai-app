import base64
import bz2
import json
import os
import uuid
import gzip
import requests
from pympler.asizeof import asizeof
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
import weaviate
from weaviate.embedded import EmbeddedOptions

from db.database import SessionLocal
from models.pdf import add_pdf
from .models import ChatPdfModel
from utils import (
    extract_text_from_pdf_content,
    parallel_compress,
    extract_pdf_name,
    process_pdf,
    process_pdf_multithreaded,
    object_handler
)
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/chatpdf", tags=["chatpdf"])


@router.post("", include_in_schema=False)
@router.post("/upload")
async def upload(chatpdf_model: ChatPdfModel):
    try:
        db = SessionLocal()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = weaviate.Client(
            embedded_options=EmbeddedOptions(),
            additional_headers={"X-OpenAI-Api-Key": openai_api_key},
        )

        pdf_id = uuid.uuid4()
        url = chatpdf_model.url
        pdf_file_name = extract_pdf_name(url)
        response = requests.get(url)
        pdf_content = response.content
        pdf_text_list = extract_text_from_pdf_content(response.content)
        size_in_mb = asizeof(pdf_content) / (1024.0**2)
        if size_in_mb > 5:
            compressed_pdf_content = gzip.compress(pdf_content)
            compression_type = "gzip"
        else:
            compressed_pdf_content = parallel_compress(pdf_content)
            compression_type = "libbzip2"

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
    
        pdf_id_str = pdf_id.__str__()
        pdf_data_inserted = add_pdf(db, pdf_id_str, pdf_file_name, compressed_pdf_content, compression_type)
        for data in result_data:
            client.data_object.create(
                {"chunk": data["chunk"]}, "Chatpdf", vector=data["embeddings"]
            )
        
        if compression_type == "gzip":
            decompressed_pdf = gzip.decompress(pdf_data_inserted["pdf"])
            pdf_data_inserted["pdf"] = base64.b64encode(decompressed_pdf).decode('utf-8')
            pdf_data_inserted = json.dumps(pdf_data_inserted, default=object_handler)
        else:
            decompressed_pdf = bz2.decompress(pdf_data_inserted["pdf"])
            pdf_data_inserted["pdf"] = base64.b64encode(decompressed_pdf).decode('utf-8')
            pdf_data_inserted = json.dumps(pdf_data_inserted, default=object_handler)

        return JSONResponse(json.loads(pdf_data_inserted))
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc
