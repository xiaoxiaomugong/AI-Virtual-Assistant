import sys
import io

# 强制设置标准输出为 UTF-8，解决 Windows 终端无法打印 emoji 或特殊字符的问题
# 在 Streamlit 中直接修改 sys.stdout.buffer 会导致 I/O operation on closed file 异常并使程序闪退。
# 已经将其注释掉，如果要解决 Windows 编码问题，请在终端设置环境变量 set PYTHONIOENCODING=utf-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 【重要修复】导入文本分割器以提前触发 tokenizers 的安全初始化。
# 在 Windows 环境下，如果不提前导入，Chroma底层的 hnswlib 会与 transformers/tokenizers 发生底层线程/DLL冲突，
# 导致在进行 similarity_search 向量检索时 Python 进程直接发生 Segmentation Fault (段错误闪退)，
# 从而表现为 Streamlit 网页在发消息时立刻关闭。
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

def print_prompt(prompt):
    print("="*20)
    print(prompt)
    print("="*20)
    return prompt

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
            if not docs:
                return "Not Found"
            formatted_str = "["
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            formatted_str = "]"
            return formatted_str

        def format_for_retriever(value):
            return value["input"]

        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input":RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever)|retriever|format_document
            }|RunnableLambda(format_for_prompt_template)|self.prompt_template|self.chat_model|StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain
    
if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    res = RagService().chain.invoke({"input": "我身高1.75米，体重75公斤，尺码推荐"}, session_config)
    print(res)