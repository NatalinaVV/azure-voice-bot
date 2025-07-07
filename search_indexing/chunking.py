def split_text(text: str, max_length: int = 500, overlap: int = 50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_length
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_length - overlap

    return chunks