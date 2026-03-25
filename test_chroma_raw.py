from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

emb = DashScopeEmbeddings(model=config.embedding_model_name)
print("Creating empty in-memory Chroma...", flush=True)
db = Chroma(embedding_function=emb)
print("Adding texts...", flush=True)
db.add_texts(["Hello world"])
print("Querying in-memory...", flush=True)
docs = db.similarity_search("Hello")
print("Found docs:", docs, flush=True)
