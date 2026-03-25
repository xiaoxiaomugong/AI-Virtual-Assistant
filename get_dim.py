print("importing", flush=True)
import chromadb
print("client", flush=True)
client = chromadb.PersistentClient(path="./chroma_db")
print("get_collection", flush=True)
collection = client.get_collection("rag")
print("count", flush=True)
print("Count:", collection.count(), flush=True)
print("get docs", flush=True)
docs = collection.get(limit=1, include=["embeddings"])
print("done get", flush=True)
if docs and docs["embeddings"]:
    print("Dim:", len(docs["embeddings"][0]))
else:
    print("No embeddings found.")
