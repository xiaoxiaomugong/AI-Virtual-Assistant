"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from datetime import datetime

def check_md5(md5_str: str):
    """
    检查传入的MD5字符串是否已经被处理过
    return False: 没有被处理过
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False
            
def save_md5(md5_str: str):
    """
    将新的MD5字符串保存到数据库中
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    """
    将输入的字符串转换为MD5格式
    """
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()  # 创建MD5对象
    md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)#如果目录不存在则创建
        self.chorma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, 
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )

    def upload_file(self, data,file_name):
        """将传入的字符串向量化后存储到数据库中"""
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "文件已存在，无需重复处理"
        
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        metadata={
                "source": file_name,
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator":"小木公"
            }
        
        self.chorma.add_texts(
            knowledge_chunks, 
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)
        return "文件上传成功"
