import os
import json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

def get_history(session_id: str) -> list:
    return FileChatMessageHistory(session_id,storage_path="./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id= session_id #会话id
        self.storage_path= storage_path #不同会话id的储存文件所在的文件夹路径
        #完整的文件路径
        self.file_path= os.path.join(self.storage_path,self.session_id)

        #确保文件是存在的
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
    
    def add_messages(self,message:Sequence[BaseMessage]) -> None:
        #Sequence序列，类似list,tuple
        all_messages= list(self.messages) #已有的消息列表
        all_messages.extend(message)  #将新的和已有的消息列表转换为字典列表

        #将数据同步到本地文件中
        new_messages=[]
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)

        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f)

    @property #装饰器将messages方法变为成员属性，调用时不需要加括号
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                messages_data=json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f)