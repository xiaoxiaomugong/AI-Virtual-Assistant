from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

emb = DashScopeEmbeddings(model=config.embedding_model_name)
print("Creating Chroma...", flush=True)
db = Chroma(
    collection_name=config.collection_name,
    embedding_function=emb,
    persist_directory=config.persist_directory
)
print("Querying in-memory...", flush=True)
docs = db.similarity_search("Hello")
print("Found docs:", docs, flush=True)
