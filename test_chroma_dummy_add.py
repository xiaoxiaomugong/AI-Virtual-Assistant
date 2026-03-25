import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

class DummyEmb(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        return [[0.1] * 1024 for _ in input]

print("Client...", flush=True)
client = chromadb.Client()
print("Collection...", flush=True)
collection = client.create_collection("test_mem", embedding_function=DummyEmb())
print("Add...", flush=True)
collection.add(documents=["Hello world"], ids=["id1"])
print("Done.", flush=True)
