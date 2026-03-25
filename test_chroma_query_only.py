from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

print("Load embeddings...", flush=True)
emb = DashScopeEmbeddings(model=config.embedding_model_name)
print("Load Chroma...", flush=True)
vector_store = Chroma(
    collection_name=config.collection_name,
    embedding_function=emb,
    persist_directory=config.persist_directory
)
print("Get Retriever...", flush=True)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
print("Invoke Retriever...", flush=True)
docs = retriever.invoke("我身高1.75米，体重75公斤，尺码推荐")
print("Docs:", len(docs), flush=True)
