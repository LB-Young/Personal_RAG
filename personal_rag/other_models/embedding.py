from FlagEmbedding import BGEM3FlagModel
from personal_rag.config import DocumentSplit_Config

class BGEEmbedding:
    def __init__(self):
        self.embedding_model = BGEM3FlagModel(DocumentSplit_Config['embedding_model_path'])

    def do_embedding(self, slices):
        print("start doing embedding !")
        embedding = self.embedding_model.encode(slices)
        print("embedding finished !")
        return embedding