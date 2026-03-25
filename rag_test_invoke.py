from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from langchain_core.runnables import RunnableWithMessageHistory

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name),
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的文档内容为基础，"
             "简洁专业地回答用户的问题。参考资料{context}"),
            ("system","并且我提供用户的历史对话记录如下："),
            MessagesPlaceholder("history"),
            ("user", "请回答用户提问：{input}")
        ])
        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()
        def format_document(docs:list[Document]):
            print("Running format_document...", flush=True)
            if not docs:
                return "Not Found"
            formatted_str = "["
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            formatted_str += "]"
            return formatted_str
        def format_for_retriever(value):
            print("Running format_for_retriever...", flush=True)
            return value["input"]
        def format_for_prompt_template(value):
            print("Running format_for_prompt_template...", flush=True)
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"] 
            return new_value
        
        def pre_llm(value):
            print("Running pre_llm...", flush=True)
            return value

        chain = (
            {
                "input":RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever)|retriever|format_document
            }|RunnableLambda(format_for_prompt_template)|self.prompt_template|RunnableLambda(pre_llm)|self.chat_model|StrOutputParser()
        )
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversation_chain

print("Start...", flush=True)
session_config = {
    "configurable":{
        "session_id":"user_001"
    }
}
try:
    rag = RagService()
    print("Invoking...", flush=True)
    res = rag.chain.invoke({"input": "我身高1.75米，体重75公斤，尺码推荐"}, session_config)
    print("DONE:", res, flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()
