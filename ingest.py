import os

DOCS_FOLDER = "docs"
CHUNK_SIZE = 500
OVERLAP = 75

def load_documents():
    documents = []
    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text
            })
    print(f"Loaded {len(documents)} document(s): {[d['source'] for d in documents]}")
    return documents

def chunk_document(text, source):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({
                "text": chunk,
                "source": source
            })
        start += CHUNK_SIZE - OVERLAP
    return chunks

def load_and_chunk_all():
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)
    print(f"Produced {len(all_chunks)} total chunks.")
    return all_chunks