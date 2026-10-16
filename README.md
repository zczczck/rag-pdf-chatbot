# RAG 智能文档问答系统

一个基于 **RAG（检索增强生成）** 的 PDF 智能问答系统：上传 PDF 文档，即可针对文档内容进行自然语言提问，AI 会基于文档内容准确回答，而不是凭空乱编。

## ✨ 功能

- 📄 上传 PDF，自动解析文档内容
- 🔍 向量检索，精准定位与问题最相关的段落
- 🤖 调用 DeepSeek 大模型，基于检索资料生成回答
- 🎨 Streamlit 网页界面，开箱即用

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install streamlit pypdf scikit-learn numpy
```

### 2. 配置 API Key

免费申请 DeepSeek API Key：https://platform.deepseek.com

**方式一（推荐）：设置环境变量**

```bash
# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="你的key"

# Linux / macOS
export DEEPSEEK_API_KEY="你的key"
```

**方式二：使用 .env 文件**

复制 `.env.example` 为 `.env`，填入你的 Key（`.env` 已在 `.gitignore` 中，不会被提交）。

### 3. 运行网页版

```bash
cd rag-pdf-chatbot
streamlit run app.py
```

## 📁 项目结构

```
rag-pdf-chatbot/
├── app.py               # 网页版（Streamlit）
├── step1_read_pdf.py    # 读 PDF + 文本切块
├── step2_retrieve.py    # 向量化 + 检索
├── step3_chat.py        # 检索 + 调大模型生成
└── make_sample_pdf.py   # 生成测试 PDF
```

## 🔗 技术链路

```
PDF 文档 → 文本解析 → 切块(chunk) → 向量化(TF-IDF)
                                          ↓
用户提问 → 向量化 → 余弦相似度检索 → 拼接 Prompt → 大模型 → 回答
```

## 🛠 技术栈

- Python
- Streamlit（网页框架）
- PyPDF（PDF 解析）
- scikit-learn（TF-IDF 向量化 + 余弦相似度）
- DeepSeek API（大模型）

## 📝 后续可优化方向

- [ ] 使用真正的 embedding 模型替代 TF-IDF
- [ ] 接入向量数据库（Chroma / FAISS）
- [ ] 按语义切块
- [ ] 多轮对话、回答引用溯源
