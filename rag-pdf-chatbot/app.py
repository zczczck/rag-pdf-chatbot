# -*- coding: utf-8 -*-
"""RAG PDF 问答机器人 —— Streamlit 网页界面。

运行：streamlit run app.py
"""

import streamlit as st

from step1_read_pdf import extract_text_from_pdf, split_text
from step2_retrieve import SimpleRetriever
from step3_chat import ask_ai_with_context

# ---------- 页面标题 ----------
st.set_page_config(page_title="RAG PDF 问答机器人", page_icon="🤖", layout="wide")

st.title("🤖 RAG PDF 问答机器人")
st.caption("上传一份 PDF，向它提问，AI 会根据文档内容准确回答（而不是凭空乱编）")

# ---------- 侧边栏：上传 PDF ----------
with st.sidebar:
    st.header("📄 第一步：上传文档")
    uploaded_file = st.file_uploader("选择 PDF 文件", type=["pdf"])

    st.divider()
    st.header("⚙️ 设置")
    top_k = st.slider("检索相关段落数量", min_value=1, max_value=5, value=3)
    st.caption("数值越大，AI 参考的资料越多")

    st.divider()
    st.markdown("**技术栈**：Python · RAG · 向量检索 · DeepSeek")
    st.markdown("**链路**：读 PDF → 切块 → 向量化 → 检索 → 生成")

# ---------- 主区域 ----------
if uploaded_file is None:
    st.info("👈 请先在左侧上传一个 PDF 文件（可以用 docs 文件夹里的示例文档）")
    st.markdown(
        """
        ### 这是什么？
        这是一个 **RAG（检索增强生成）问答机器人**：
        大模型不知道你文档里的内容，这个应用会先把文档切碎、转成向量存起来，
        你提问时先检索最相关的段落，再让大模型"看着资料回答"。

        ### 试试看
        1. 左侧上传 `docs/AI应用开发入门指南.pdf`
        2. 问它："什么是 RAG？"
        3. 再问："苹果手机多少钱？" —— 看它如何诚实回答"资料里没有"
        """
    )
else:
    # 读取上传的 PDF（Streamlit 上传的文件需要读成字节流）
    st.success(f"✅ 已加载文档：{uploaded_file.name}")

    # 把上传的文件存到临时位置，供 pypdf 读取
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    # 用缓存：同一份文档只解析一次，避免重复计算
    @st.cache_resource
    def build_retriever(path: str):
        text = extract_text_from_pdf(path)
        chunks = split_text(text)
        return SimpleRetriever(chunks), len(chunks), len(text)

    retriever, num_chunks, num_chars = build_retriever(tmp_path)
    st.caption(f"文档共 {num_chars} 字，切成 {num_chunks} 块")

    st.divider()

    # 问答区域
    st.header("💬 提问")
    question = st.text_input("输入你的问题，然后回车：", placeholder="例如：什么是 RAG？")

    if question:
        with st.spinner("正在检索并生成回答..."):
            # 检索
            context = retriever.search(question, top_k=top_k)
            # 生成
            answer = ask_ai_with_context(question, context)

        # 展示回答
        st.markdown("### 🧠 AI 回答")
        st.write(answer)

        # 展示检索到的原始资料，便于查看 RAG 的检索过程
        with st.expander("🔍 查看检索到的原始资料（RAG 的检索结果）"):
            for i, c in enumerate(context, 1):
                st.markdown(f"**片段 {i}：**")
                st.text(c[:300])
                st.divider()
