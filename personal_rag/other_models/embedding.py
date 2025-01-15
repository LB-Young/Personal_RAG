import requests
import json
from together import Together
from FlagEmbedding import BGEM3FlagModel
from personal_rag.config import DocumentSplit_Config, get_api_key

class BGEEmbedding:
    def __init__(self):
        self.embedding_mode = DocumentSplit_Config['embedding_mode']
        if self.embedding_mode == "remote":
            self.embedding_url = DocumentSplit_Config["embedding_remote_url"]
        else:
            self.embedding_url = None
        if self.embedding_mode == "local":
            self.embedding_model = BGEM3FlagModel(DocumentSplit_Config['embedding_model_path'])
        else:
            self.embedding_model = None
        if self.embedding_mode == "together":
            api_key = get_api_key("together")
            self.client = Together(api_key=api_key)

    def do_embedding(self, slices):
        print("start doing embedding !")
        if self.embedding_mode == "remote":
            embedding = self.do_embedding_remote(slices)
        elif self.embedding_mode == "local":
            embedding = self.embedding_model.encode(slices)
        elif self.embedding_mode == "together":
            slices_500 = []
            for slice in slices:
                if len(slice) > 500:
                    slices_500.append(slice[:500])
                else:
                    slices_500.append(slice)
            response = self.client.embeddings.create(
            model="BAAI/bge-base-en-v1.5",
            input=slices_500
            )
            embedding = []
            for item in response.data:
                embedding.append(item.embedding)
        else:
            raise ValueError("embedding_mode must be remote or local or together")
        
        print("embedding finished !")
        return embedding
    
    def do_embedding_remote(self, slices):
        print("start doing embedding !")
        headers = ["Content-Type", "application/json"]
        response = requests.post(self.embedding_url, headers=headers, data={"slices": slices})
        response.encoding = "utf-8"
        embedding = response.json()["embedding"]
        print("embedding finished !")
        return embedding
    
