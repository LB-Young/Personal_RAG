from personal_rag.config import RAG_Config
from personal_rag.other_models.rerank import BGERerank
from personal_rag.other_models.remote_rerank import CohereRerank

class RerankClient:
    def __init__(self):
        if RAG_Config['rank_method'] == "local_rerank":
            self.rerank_client = BGERerank()
        elif RAG_Config['rank_method'] == "cohere_rerank":
            self.rerank_client = CohereRerank()
        else:
            raise ValueError("rank_method must be local_rerank or remote_rerank")

    def do_rerank(self, query_entity):
        retrival_slices = query_entity.retrival_slices
        query = query_entity.query
        slice_contents = [slice['slice_content'] for slice in retrival_slices]
        scores = self.rerank_client.ado_rerank(query, slice_contents)
        for index, item in enumerate(retrival_slices):
            item['rerank_scores'] = scores[index]
        retrival_slices.sort(key=lambda x: x['rerank_scores'])
        return retrival_slices