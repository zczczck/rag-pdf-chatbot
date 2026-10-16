# -*- coding: utf-8 -*-
"""PDF 文本提取与切分。"""

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """读取 PDF 文件，返回其中的全部文字。"""
    reader = PdfReader(pdf_path)
    all_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)
    return "\n".join(all_text)


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """将长文本按固定长度切分为 chunk，相邻 chunk 之间保留 overlap 重叠。

    chunk_size: 每个 chunk 的最大字符数
    overlap: 相邻 chunk 重叠的字符数，用于避免句子在边界处被截断
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


if __name__ == "__main__":
    import sys

    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "../docs/示例文档.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    print(f"共 {len(text)} 字，切成 {len(chunks)} 块")
    print(chunks[0][:300])
