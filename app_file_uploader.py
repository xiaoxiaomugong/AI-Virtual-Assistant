"""
基于Streamlit完成WEB网页上传文件
"""
import time
import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务")
uploader_file = st.file_uploader(
    "上传TXT文件",
    type=["txt"],
    accept_multiple_files=False,
)

#session_state是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size//1024  # 转换为KB
    st.subheader(f"文件名称: {file_name}")
    st.write(f"文件类型: {file_type}")
    st.write(f"文件大小: {file_size:.2f} KB")

    text = uploader_file.read().decode("utf-8")

    with st.spinner("正在上传文件..."):
        time.sleep(1)  # 模拟上传过程中的等待时间
        result = st.session_state["service"].upload_file(text,file_name)
        st.write(result)
    