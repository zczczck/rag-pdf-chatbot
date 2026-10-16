# -*- coding: utf-8 -*-
"""
AI 客服机器人 —— 网页版（Streamlit）

运行：streamlit run app.py

功能：带多轮对话记忆的电商客服，支持：
    - 连续多轮对话，AI 记住上下文
    - 一键清空重新开始
    - 查看完整对话历史
"""

import streamlit as st

from customer_service import CustomerServiceBot

st.set_page_config(page_title="AI 客服机器人", page_icon="🎧", layout="wide")

st.title("🎧 AI 客服机器人")
st.caption("带多轮对话记忆的智能客服 —— 它能记住你们刚才聊了什么")

# 侧边栏：说明 + 清空按钮
with st.sidebar:
    st.header("关于本项目")
    st.markdown(
        """
        **技术亮点：多轮对话记忆**
        
        普通 AI 每次提问都是"失忆"的，而本客服会把历史对话存起来，
        每次提问时连同上下文一起发给大模型，从而"记住"之前聊了什么。
        
        **技术栈**：Python · Streamlit · 大模型 API · 上下文管理
        """
    )
    st.divider()
    if st.button("🔄 清空对话，重新开始", use_container_width=True):
        st.session_state.bot.reset()
        st.session_state.history = []
        st.rerun()

# 初始化机器人（存到 session_state，保证刷新页面不丢记忆）
if "bot" not in st.session_state:
    st.session_state.bot = CustomerServiceBot()
if "history" not in st.session_state:
    st.session_state.history = []

bot = st.session_state.bot

# 显示历史对话
st.header("💬 对话")
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

# 输入框
st.divider()
user_input = st.chat_input("向客服小智提问，例如：我想退货...")

if user_input:
    # 显示用户消息
    st.session_state.history.append({"role": "user", "content": user_input})
    with chat_container:
        st.chat_message("user").write(user_input)

    # 获取客服回复
    with st.spinner("小智正在思考..."):
        reply = bot.chat(user_input)

    st.session_state.history.append({"role": "assistant", "content": reply})
    with chat_container:
        st.chat_message("assistant").write(reply)
    st.rerun()
