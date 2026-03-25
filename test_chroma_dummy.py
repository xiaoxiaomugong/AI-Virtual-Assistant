from langchain_chroma import Chroma
import config_data as config

class DummyEmb:
    def embed_query(self, text):
        return [0.1] * 1024
    def embed_documents(self, texts):
        return [[0.1] * 1024 for _ in texts]

print("Load Chroma with dummy...", flush=True)
vector_store = Chroma(
    collection_name=config.collection_name,
    embedding_function=DummyEmb(),
    persist_directory=config.persist_directory
)
print("Invoke Retriever...", flush=True)
docs = vector_store.similarity_search("我身高1.75米，体重75公斤，尺码推荐")
print("Docs:", len(docs), flush=True)
