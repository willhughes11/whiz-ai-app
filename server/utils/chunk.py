import nltk


def chunk_text(text: str, max_chunk_length: int):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Calculate the number of chunks based on the specified length
    num_chunks = len(tokens) // max_chunk_length + (len(tokens) % max_chunk_length > 0)

    # Create chunks
    chunks = [
        tokens[i * max_chunk_length : (i + 1) * max_chunk_length]
        for i in range(num_chunks)
    ]

    # Convert chunks back to text
    chunked_text = [" ".join(chunk) for chunk in chunks]

    return chunked_text
