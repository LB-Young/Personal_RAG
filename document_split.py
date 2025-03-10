import os
print(os.path.dirname(__file__))

from personal_rag.document_split.document_extractor import DocumentExtractor

"""
file_path: file_path or dir_path
db_type:choose from "chromadb", "local"
"""

file_path = r"F:\学习资料\学习笔记office\微调\PEFT.docx"

res = DocumentExtractor(file_path, need_embedding=True, db_name="test", db_type="local").do_extract()
print("documents extract finished!")