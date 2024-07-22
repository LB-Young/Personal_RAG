from personal_rag.document_split.extractor.types.docx_extractor import DocxExtractor
from personal_rag.document_split.extractor.types.pdf_extractor import PDFExtractor

class Extractor_Factory:
    def get_extractor_processor(ext):
        if ext == "docx":
            return DocxExtractor()
        elif ext == "pdf":
            return PDFExtractor()