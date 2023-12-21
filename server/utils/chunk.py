import nltk


def chunk_text(text: str, max_chunk_length: int, overlap: int = 0):
    tokens = nltk.word_tokenize(text)
    step_size = max_chunk_length - overlap
    num_chunks = (len(tokens) - overlap) // step_size + 1

    chunks = [
        tokens[i * step_size : i * step_size + max_chunk_length]
        for i in range(num_chunks)
    ]

    chunked_text = [" ".join(chunk) for chunk in chunks]

    return chunked_text
