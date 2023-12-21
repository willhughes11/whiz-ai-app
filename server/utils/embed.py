import torch
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModel


def embed_text(text: str):
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    tokens = tokenizer([text], return_tensors="pt")
    with torch.no_grad():
        output = model(**tokens).last_hidden_state
    avg_pooled = output.mean(dim=1)
    return avg_pooled.tolist()[0]


def embed_chunk(chunk: list[str], tokenizer, model):
    tokens = tokenizer(chunk, return_tensors="pt")
    with torch.no_grad():
        output = model(**tokens).last_hidden_state
    avg_pooled = output.mean(dim=1)
    return {"chunk": chunk, "embeddings": avg_pooled.tolist()[0]}


def embed_chunked_text(chunked_text: list[str]):
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    with ThreadPoolExecutor() as executor:
        chunk_and_embeddings = list(
            executor.map(
                embed_chunk,
                chunked_text,
                [tokenizer] * len(chunked_text),
                [model] * len(chunked_text),
            )
        )

    return chunk_and_embeddings
