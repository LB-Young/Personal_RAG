import os
print(os.path.dirname(__file__))

from personal_rag.document_split.document_extractor import DocumentExtractor

file_path = r"F:\学习资料\NLP论文\大模型\摘要阅读\笔记.docx"
res = DocumentExtractor(file_path).do_extract()
print(res)