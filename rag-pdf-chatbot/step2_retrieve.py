# -*- coding: utf-8 -*-
"""向量检索：基于 TF-IDF 向量化与余弦相似度的文本检索。"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimpleRetriever:
    """基于 TF-IDF 的向量检索器（RAG 中的检索部分）。"""

    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer()
        self.chunk_vectors = self.vectorizer.fit_transform(chunks)

    def search(self, question: str, top_k: int = 3) -> list[str]:
        """返回与问题最相似的 top_k 个文本块。"""
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.chunk_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]


if __name__ == "__main__":
    sample_chunks = [
        "大模型不知道训练数据之外的新内容。",
        "RAG 是检索增强生成，先检索再回答。",
        "今天天气很好，适合出去散步。",
        "向量检索通过计算相似度找到最相关的段落。",
    ]
    retriever = SimpleRetriever(sample_chunks)
    results = retriever.search("什么是 RAG？", top_k=2)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")
