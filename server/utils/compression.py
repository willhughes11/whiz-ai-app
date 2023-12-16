import bz2
import concurrent.futures

def parallel_compress(data):
    compressed_chunks = []
    chunk_size = 1024 * 1024  # 1 MB chunks

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(bz2.compress, data[i : i + chunk_size]): i
            for i in range(0, len(data), chunk_size)
        }

        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            compressed_chunk = future.result()
            compressed_chunks.append((index, compressed_chunk))

    # Sort the results based on the original order
    compressed_chunks.sort(key=lambda x: x[0])

    compressed_data = b"".join(chunk[1] for chunk in compressed_chunks)
    return compressed_data