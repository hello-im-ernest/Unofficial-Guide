import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_and_chunk_all

COLLECTION_NAME = "unofficial_guide"
TOP_K = 6

_client = chromadb.PersistentClient(path="./chroma_db")
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store():
    chunks = load_and_chunk_all()
    
    try:
        _client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    collection = _client.create_collection(COLLECTION_NAME)
    
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = _model.encode(texts).tolist()
    metadatas = [{"source": s} for s in sources]
    
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")
    return collection

def get_collection():
    return _client.get_collection(COLLECTION_NAME)

def retrieve(query, n_results=TOP_K):
    collection = get_collection()
    query_embedding = _model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks