from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
emb = DashScopeEmbeddings(model=config.embedding_model_name)
print("Embedding query...", flush=True)
res = emb.embed_query("Hello world")
print("Len:", len(res), flush=True)
print("Embedding documents...", flush=True)
res2 = emb.embed_documents(["Hello world"])
print("Len doc:", len(res2), flush=True)
