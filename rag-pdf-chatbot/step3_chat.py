# -*- coding: utf-8 -*-
"""RAG 生成：将检索到的资料与用户问题拼接为 Prompt，调用大模型生成回答。"""

import sys
import json
import os
import urllib.request

from step1_read_pdf import extract_text_from_pdf, split_text
from step2_retrieve import SimpleRetriever

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")


def ask_ai_with_context(question: str, context: list[str]) -> str:
    """将检索结果与用户问题拼接，调用大模型基于资料回答。"""
    context_text = "\n\n".join(context)

    prompt = f"""请根据下面提供的资料回答用户的问题。

【资料】
{context_text}

【用户问题】
{question}

【要求】
1. 只根据上面的资料回答，不要编造资料里没有的内容。
2. 如果资料里没有答案，请直接说"资料中没有相关信息"。
"""

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "../docs/AI应用开发入门指南.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    retriever = SimpleRetriever(chunks)

    print(f"文档已加载，切成 {len(chunks)} 块。输入问题，输入 quit 退出。")

    while True:
        question = input("你：").strip()
        if question.lower() in ("quit", "exit", "退出"):
            break
        if not question:
            continue
        context = retriever.search(question, top_k=3)
        answer = ask_ai_with_context(question, context)
        print(f"AI：{answer}\n")


if __name__ == "__main__":
    main()
