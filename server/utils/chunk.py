import nltk


def chunk_text(text, max_chunk_length, overlap=0):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Calculate the number of chunks based on the specified length and overlap
    step_size = max_chunk_length - overlap
    num_chunks = (len(tokens) - overlap) // step_size + 1

    # Create chunks with overlap
    chunks = [
        tokens[i * step_size : i * step_size + max_chunk_length]
        for i in range(num_chunks)
    ]

    # Convert chunks back to text
    chunked_text = [" ".join(chunk) for chunk in chunks]

    return chunked_text
