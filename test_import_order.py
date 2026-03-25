from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

emb = DashScopeEmbeddings(model="text-embedding-v4")
db = Chroma(
    collection_name="rag",
    embedding_function=emb,
    persist_directory="./chroma_db"
)
docs = db.similarity_search("Hello")
print("Found docs:", len(docs))
