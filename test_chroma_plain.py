import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

class MyEF(EmbeddingFunction):
    def __init__(self):
        self.emb = DashScopeEmbeddings(model=config.embedding_model_name)
    def __call__(self, input: Documents) -> Embeddings:
        print("Embedding called!", flush=True)
        res = self.emb.embed_documents(input)
        print("Embedding done!", flush=True)
        return res

print("Client...", flush=True)
client = chromadb.Client()
print("Collection...", flush=True)
collection = client.create_collection("test", embedding_function=MyEF())
print("Add...", flush=True)
collection.add(documents=["Hello world"], ids=["id1"])
print("Query...", flush=True)
res = collection.query(query_texts=["Hello"], n_results=1)
print("Res:", res, flush=True)
