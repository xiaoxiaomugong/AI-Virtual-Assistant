print("T1", flush=True)
import sys
print("T2", flush=True)
from vector_stores import VectorStoreService
print("T3", flush=True)
from langchain_community.embeddings import DashScopeEmbeddings
print("T4", flush=True)
import config_data as config
print("T5", flush=True)
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
print("T6", flush=True)
from langchain_community.chat_models import ChatTongyi
print("T7", flush=True)
from langchain_core.documents import Document
print("T8", flush=True)
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
print("T9", flush=True)
from langchain_core.output_parsers import StrOutputParser
print("T10", flush=True)
from file_history_store import get_history
print("T11", flush=True)
from langchain_core.runnables import RunnableWithMessageHistory

print("Start...", flush=True)
