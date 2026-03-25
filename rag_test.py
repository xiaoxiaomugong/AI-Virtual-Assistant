import sys
print("RAG_IMP: 1")
import io
print("RAG_IMP: 2")

from vector_stores import VectorStoreService
print("RAG_IMP: 3")
from langchain_community.embeddings import DashScopeEmbeddings
print("RAG_IMP: 4")
import config_data as config
print("RAG_IMP: 5")
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
print("RAG_IMP: 6")
from langchain_community.chat_models import ChatTongyi
print("RAG_IMP: 7")
from langchain_core.documents import Document
print("RAG_IMP: 8")
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
print("RAG_IMP: 9")
from langchain_core.output_parsers import StrOutputParser
print("RAG_IMP: 10")
from file_history_store import get_history
print("RAG_IMP: 11")
from langchain_core.runnables import RunnableWithMessageHistory
print("RAG_IMP: 12")

class RagService(object):
    pass
print("RAG_IMP: DONE")