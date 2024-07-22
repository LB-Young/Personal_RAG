import os
print(os.path.dirname(__file__))

from personal_rag.document_split.document_extractor import DocumentExtractor

file_path = "xxxx"
res = DocumentExtractor(file_path).do_extract()
print("documents extract finished!")