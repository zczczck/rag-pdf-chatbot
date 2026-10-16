# -*- coding: utf-8 -*-
"""AI 客服机器人核心：具备多轮对话记忆的智能客服。

通过维护消息历史列表，每轮请求将完整历史与当前问题一并发送给大模型，
使其能够记住对话上下文。
"""

import json
import os
import urllib.request

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

SYSTEM_PROMPT = """你是一家电商平台的客服助手"小智"。
你的职责：
1. 用友好、专业的语气回答用户关于订单、退换货、物流、售后的咨询。
2. 如果用户问的问题需要更多信息（如订单号），主动引导用户提供。
3. 回答简洁，每次控制在 3 句话以内。
请始终保持礼貌，用中文回答。"""


class CustomerServiceBot:
    """带多轮对话记忆的客服机器人。"""

    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

    def chat(self, user_input: str) -> str:
        """处理一次用户输入，返回回复并更新对话历史。"""
        self.messages.append({"role": "user", "content": user_input})

        body = {
            "model": "deepseek-chat",
            "messages": self.messages,
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

        reply = result["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        """清空对话历史。"""
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


if __name__ == "__main__":
    if not API_KEY:
        print("请先设置环境变量 DEEPSEEK_API_KEY")
    else:
        bot = CustomerServiceBot()
        while True:
            user = input("你：").strip()
            if user.lower() in ("quit", "exit", "退出"):
                break
            if not user:
                continue
            reply = bot.chat(user)
            print(f"小智：{reply}\n")
