import os
import sys

from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

print("Testing DashScopeEmbeddings", flush=True)
try:
    emb = DashScopeEmbeddings(model=config.embedding_model_name)
    res = emb.embed_query("我身高1.75米，体重75公斤，尺码推荐")
    print("Embeddings got:", len(res), flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()
print("Done Embeddings.", flush=True)

print("Testing Chroma", flush=True)
from vector_stores import VectorStoreService
try:
    vec = VectorStoreService(embedding=emb)
    retriever = vec.get_retriever()
    print("Retriever created.", flush=True)
    docs = retriever.invoke("我身高1.75米，体重75公斤，尺码推荐")
    print("Docs got:", len(docs), flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()
print("Done Chroma.", flush=True)
