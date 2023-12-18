import fitz
import os
from concurrent.futures import ThreadPoolExecutor
from .chunk import chunk_text
from .embed import embed_chunked_text

def extract_text_from_pdf_content(pdf_content: bytes):
    try:
        text_per_page = []
        pdf_document = fitz.open("pdf", pdf_content)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_per_page.append(page.get_text())

        pdf_document.close()

        return text_per_page
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_pdf_name(pdf_url: str):
    pdf_name = os.path.basename(pdf_url)
    pdf_name = pdf_name.split('?')[0].split('#')[0]

    return pdf_name

def process_pdf(pdf_id: str, pdf_file_name: str, pdf_text_list: list[str], chunk_threshold: int, token_overlap: int):
    chunked_pdf_data = []
    for text_index, text in enumerate(pdf_text_list):
        chunked_text = chunk_text(text, chunk_threshold, token_overlap)
        chunked_and_embedded_text = embed_chunked_text(chunked_text)
        for chunk_index, chunk in enumerate(chunked_and_embedded_text):
            chunked_pdf_data.append(
                {
                    "source": f"{pdf_id}",
                    "source_page": f"{pdf_id}-{text_index}",
                    "file": pdf_file_name,
                    "file_page": f"{pdf_file_name}-{text_index}",
                    "chunk": chunk["chunk"],
                    "chunk_index": chunk_index,
                    "embeddings": chunk["embeddings"],
                }
            )
    
    return chunked_pdf_data

def process_pdf_multithreaded(pdf_id: str, pdf_file_name: str, pdf_text_list: list[str], chunk_threshold: int, token_overlap: int):
    chunked_pdf_data = []

    def process_chunk(index, text):
        chunked_text = chunk_text(text, chunk_threshold, token_overlap)
        chunked_and_embedded_text = embed_chunked_text(chunked_text)
        return [
            {
                "source": f"{pdf_id}",
                "source_page": f"{pdf_id}-{index}",
                "file_name": pdf_file_name,
                "chunk": chunk["chunk"],
                "embeddings": chunk["embeddings"],
            }
            for chunk in chunked_and_embedded_text
        ]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, range(len(pdf_text_list)), pdf_text_list))
        
    chunked_pdf_data = [item for sublist in results for item in sublist]

    return chunked_pdf_data