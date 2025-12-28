from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings

from typing import Any
import constant
import memory

_db = None

def init_retrieval():
    global _db
    if _db is None:
        # 确保记忆系统已初始化
        client = memory._qdrant_client
        embedding_model = SentenceTransformerEmbeddings(model_name=constant.embedding_model_name)

        
        if client is None or embedding_model is None:
            raise ValueError("记忆系统未初始化，请先调用 memory.init_memory_system()")
        
        # 初始化向量存储
        _db = QdrantVectorStore(
            client=client,
            embedding=embedding_model,
            collection_name=f"{constant.agent_name}_db"
        )
    return _db

def similarity_search_with_reranking(query: str, k=5) -> list[Any]:
    # 向量检索
    initial_docs = _db.similarity_search_with_score(query=query, k=k*5)
    
    if not initial_docs:
        return []
    
    # 准备数据
    documents = [doc for doc, _ in initial_docs]
    cosine_scores = [score for _, score in initial_docs]
    
    # 第二阶段：CrossEncoder重排序
    # 创建(query, document)对
    pairs = [(query, doc.page_content) for doc in documents]
    
    # 使用CrossEncoder预测相关性分数
    rerank_scores = memory._reranker_model.predict(pairs)
    
    # 组合并排序
    results = list(zip(documents, rerank_scores, cosine_scores))
    results.sort(key=lambda x: x[1], reverse=True)  # 按CrossEncoder分数降序
    
    # 返回前k个结果
    return [doc.page_content for doc, _, _ in results[:k]]
    