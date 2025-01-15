import os
print(os.path.dirname(__file__))

from personal_rag.document_split.document_extractor import DocumentExtractor

file_path = r"C:\Users\86187\Desktop\AceMath_ Advancing Frontier Math Reasoning with Post-Training and Reward Modeling.pdf"
res = DocumentExtractor(file_path).do_extract()
print(res)