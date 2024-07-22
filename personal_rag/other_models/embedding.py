from FlagEmbedding import BGEM3FlagModel


class BGEEmbedding:
    def __init__(self, model_path):
        self.embedding_model = BGEM3FlagModel(model_path)

    def do_embedding(self, slices):
        embedding = self.embedding_model.encode(slices)
        return embedding