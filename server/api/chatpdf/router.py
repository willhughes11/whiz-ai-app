import base64
import bz2
import json
import os
import uuid
import gzip
import requests
from pympler.asizeof import asizeof
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import APIRouter, HTTPException
from litellm import completion

import weaviate
from weaviate.embedded import EmbeddedOptions

from dotenv import load_dotenv

load_dotenv()

from db.database import SessionLocal
from models.pdf import add_pdf, get_pdf_by_id
from .models import ChatPdfModel, ChatPdfUploadModel
from .prompts import chatpdf_prompt
from utils import (
    embed_text,
    extract_text_from_pdf_content,
    parallel_compress,
    extract_pdf_name,
    process_pdf,
    process_pdf_multithreaded,
    object_handler,
)
from config import VECTOR_DB_CLASS_NAME

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


router = APIRouter(prefix="/chatpdf", tags=["chatpdf"])


@router.post("/")
async def chatpdf(chatpdf: ChatPdfModel):
    db = SessionLocal()
    client = weaviate.Client(
        embedded_options=EmbeddedOptions(),
        additional_headers={"X-OpenAI-Api-Key": OPENAI_API_KEY},
    )

    history = chatpdf.history
    model = chatpdf.model
    pdf_id = chatpdf.id

    pdf_data = get_pdf_by_id(db, pdf_id)

    question = history[-1]["content"]
    vector = embed_text(question)

    docs = (
        client.query.get(
            class_name=VECTOR_DB_CLASS_NAME,
            properties=["chunk", "source_page", "file_page"],
        )
        .with_hybrid(query=question, vector=vector)
        .with_where(
            {
                "path": ["source"],
                "operator": "Equal",
                "valueText": pdf_id,
            }
        )
        .with_limit(3)
        .do()
    )

    source_list = [
        f"{doc['file_page']}: {doc['chunk']}" for doc in docs["data"]["Get"]["Chatpdf"]
    ]
    sources_str = "\n".join(source_list)

    system_prompt = chatpdf_prompt.format(
        pdf_title=pdf_data["title"],
        num_pages=pdf_data["num_pages"],
        sources=sources_str,
    )

    history.insert(0, {"role": "system", "content": system_prompt})

    ollama_api_base = "http://localhost:11434"
    api_base = ollama_api_base if "ollama" in model else None

    print(history)

    def generate_responses():
        response = completion(
            model=model,
            messages=history,
            api_base=api_base,
            stream=True,
        )

        answer = ""
        for chunk in response:
            answer += chunk.choices[0].delta.content
            yield json.dumps({"role": "assistant", "content": answer})
        else:
            print(json.dumps({"role": "assistant", "content": answer}))

    return StreamingResponse(generate_responses(), media_type="text/event-stream")


@router.post("/upload")
async def upload(model: ChatPdfUploadModel):
    try:
        db = SessionLocal()

        client = weaviate.Client(
            embedded_options=EmbeddedOptions(),
            additional_headers={"X-OpenAI-Api-Key": OPENAI_API_KEY},
        )

        pdf_id = uuid.uuid4()
        url = model.url
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
        pdf_data_inserted = add_pdf(
            db,
            pdf_id_str,
            pdf_file_name,
            compressed_pdf_content,
            len(pdf_text_list),
            compression_type,
        )

        for data in result_data:
            client.data_object.create(
                data, VECTOR_DB_CLASS_NAME, vector=data["embeddings"]
            )

        if pdf_data_inserted["compression_type"] == "gzip":
            decompressed_pdf = gzip.decompress(pdf_data_inserted["pdf"])
        else:
            decompressed_pdf = bz2.decompress(pdf_data_inserted["pdf"])

        pdf_data_inserted.pop("compression_type")
        pdf_data_inserted["pdf"] = base64.b64encode(decompressed_pdf).decode("utf-8")
        pdf_data_inserted = json.dumps(pdf_data_inserted, default=object_handler)

        return JSONResponse(json.loads(pdf_data_inserted))
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc


@router.get("/pdf/{pdf_id}")
async def get_pdf(pdf_id: str):
    db = SessionLocal()
    pdf_data = get_pdf_by_id(db, pdf_id)

    if pdf_data["compression_type"] == "gzip":
        decompressed_pdf = gzip.decompress(pdf_data["pdf"])
    else:
        decompressed_pdf = bz2.decompress(pdf_data["pdf"])

    pdf_data.pop("compression_type")
    pdf_data["pdf"] = base64.b64encode(decompressed_pdf).decode("utf-8")
    pdf_data = json.dumps(pdf_data, default=object_handler)

    return JSONResponse(json.loads(pdf_data))
