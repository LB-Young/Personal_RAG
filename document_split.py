import os
print(os.path.dirname(__file__))

from personal_rag.document_split.document_extractor import DocumentExtractor

file_path = r"E:\Microsoft Edge\myfile.pdf"
res = DocumentExtractor(file_path).do_extract()
print(res)