from langchain.tools import tool
from typing import Any
import time
import constant
import os
import datetime
import subprocess
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


_qdrant_client = None
_embedding_model = None
_reranker_model = None

def init_memory_system():
    """初始化记忆系统，在调用 CustomMiddleware 之前调用"""
    global _qdrant_client, _embedding_model,_reranker_model
    
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(url=constant.url)
    
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(constant.embedding_model_name)
    
    if _reranker_model is None:
        _reranker_model = CrossEncoder(constant.reranker_model_name)
        
    
    # 创建或重建集合
    _qdrant_client.recreate_collection(
        collection_name=f"{constant.agent_name}_db",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    
    return True

def update_db(resp:list, i:int) -> str:
    """resp: response
       i: turn number
    """
    try:
        # 拆分resp
        conversation_text = ""
        for msg in resp:
            if hasattr(msg, 'content'):
                msg_type = "Human" if "HumanMessage" in str(type(msg)) else "AI"
                conversation_text += f"{msg_type}: {msg.content}\n"
        
        if not conversation_text.strip():
            return f"对话轮次 {i} 的文本为空，跳过存储"
        
        # txt2v
        vector = _embedding_model.encode(conversation_text).tolist()
            
        # 创建数据点
        point = PointStruct(
            id=i,
            vector=vector,
            payload={
                "text": conversation_text,
                "turn_id": i,
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
            
        _qdrant_client.upsert(collection_name=f"{constant.agent_name}_db", points=[point])
        print("update memory database!")
    except Exception as e:
        return f"cannot update memory database! ({e})"
    



def create_txt_file(filename, initial_content=""):
    try:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(initial_content)
            return f"文件 '{filename}' 创建成功！"
        else:
            return f"文件 '{filename}' 已存在，跳过创建"
    except Exception as e:
        return f"创建文件时出错: {e}"
    
def append_to_file(filename, content):
    """add the new dialogue to text for retrieve."""
    try:
        if isinstance(content, list):
            text_content = ""
            for msg in content:
                if hasattr(msg, 'content'):
                    msg_type = "Human" if "HumanMessage" in str(type(msg)) else "AI"
                    text_content += f"{msg_type}: {msg.content}\n"
            content_to_write = text_content.strip()
        else:
            content_to_write = str(content)
        with open(filename, 'a', encoding='utf-8') as f:
            if os.path.getsize(filename) > 0:
                f.write('\n')
            f.write(content_to_write)
        print(f"内容已追加到 {filename}")
    except Exception as e:
        return f"Cannot save the response this turn. ({e})"
    
    
        
        
    
    
    
    
    