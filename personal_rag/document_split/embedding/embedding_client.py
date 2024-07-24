from personal_rag.other_models.embedding import BGEEmbedding

class EmbeddingClient:
    def __init__(self):
        self.embedding = BGEEmbedding()

    def do_embedding(self, slices):
        for key in slices.keys():
            all_content = [slice['slice_content'] for slice in slices[key]]
            all_embeddings = self.embedding.do_embedding(all_content)
            for index, item in enumerate(slices[key]):
                item['embedding'] = all_embeddings['dense_vecs'][index].tolist()
        return slices