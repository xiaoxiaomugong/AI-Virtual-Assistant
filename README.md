# AI Virtual Assistant (智能客服与知识库系统)

这是一个基于RAG (Retrieval-Augmented Generation，检索增强生成) 技术的智能客服和文档问答系统。项目使用 Streamlit 构建可视化交互界面，结合本地或云端大模型（如阿里云 DashScope/通义千问）和 ChromaDB 向量数据库，实现基于自有知识库的智能问答。

## 项目特点

- **智能问答交互**: 提供类似 ChatGPT 的 Web 对话界面，支持多轮对话与流式输出。
- **本地知识库上传**: 支持用户上传自有文档，系统自动提取、切分并进行向量化存储。
- **高效检索**: 集成 ChromaDB 本地向量数据库，确保数据隐私与快速的相似度检索。
- **RAG 架构**: 基于先进的 RAG 理念，大模型的回答将严格基于检索到的知识库内容，减少“幻觉”。
- **灵活的配置**: 支持自定义大模型接口（如 DashScope）、嵌入模型和向量库配置。

## 项目结构

- `app_qa.py`: 智能客服主界面（Streamlit 聊天应用）。
- `app_file_uploader.py`: 知识库管理与文件上传界面。
- `rag.py`: RAG 核心服务类，负责大语言模型链（Chain）的组装、提示词构建和检索逻辑。
- `knowledge_base.py`: 知识库文档处理模块，负责文件的解析、文本切分（Chunking）等工作。
- `vector_stores.py`: 向量数据库操作模块，封装了针对 ChromaDB 的数据插入、检索和管理逻辑。
- `file_history_store.py`: 文件上传历史与处理状态的管理记录。
- `config_data.py`: 全局配置文件（包含 API Key、模型名称、数据库路径等参数）。
- `chroma_db/`: 本地向量数据库的默认持久化存储目录。
- `data/`: 上传文档和相关数据的存储目录。

## 环境依赖

本项目主要依赖于以下库（具体版本和全量库建议使用 `pip freeze > requirements.txt` 导出）：

- `streamlit`
- `langchain` / `langchain-community`
- `chromadb`
- 相关的 LLM SDK (如 `dashscope` 等)

## 安装与运行

### 1. 准备环境

建议使用 Python 3.8+ 版本，并创建虚拟环境：

```bash
python -m venv venv
# Windows 激活方式
.\venv\Scripts\activate
# Linux/Mac 激活方式
source venv/bin/activate
```

### 2. 配置参数

在运行前，请确保在 `config_data.py` 或系统环境变量中配置好您的大模型 API 密钥（例如 `DASHSCOPE_API_KEY`）及相关路径。

### 3. 运行文件上传与知识库构建应用

启动文件上传应用，将您的本地文档录入系统：

```bash
streamlit run app_file_uploader.py
```

在浏览器中打开生成的本地链接，上传所需文档进行向量化处理。

### 4. 运行智能问答客户端

启动对话界面，开始向智能助理提问：

```bash
streamlit run app_qa.py
```

## 注意事项

- 在使用 DashScope 等外部 API 时，请确保网络通畅及账户余额充足。
- 对于本地 ChromaDB，如果遇到兼容性问题（如 sqlite3 版本过低），请根据官方文档升级相关环境。
- 当前项目包含较多测试脚本（`test_*.py`、`debug_*.py`），您可以参考这些脚本了解底层组件（如 ChromaDB 连接、大模型直调）的具体使用方法。

## 许可证

MIT License (或根据实际项目需求补充)