import torch
import concurrent.futures
from transformers import AutoTokenizer, AutoModel


def embed_chunk(chunk, tokenizer, model):
    tokens = tokenizer(chunk, return_tensors="pt")
    with torch.no_grad():
        output = model(**tokens).last_hidden_state
    avg_pooled = output.mean(dim=1)
    return {"chunk": chunk, "embeddings": avg_pooled.tolist()[0]}


def embed_chunked_text(chunked_text: list[str]):
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    chunk_and_embeddings = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_chunk = {
            executor.submit(embed_chunk, chunk, tokenizer, model): chunk
            for chunk in chunked_text
        }
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                result = future.result()
                chunk_and_embeddings.append(result)
            except Exception as e:
                print(f"Error embedding chunk '{chunk}': {e}")

    return chunk_and_embeddings
