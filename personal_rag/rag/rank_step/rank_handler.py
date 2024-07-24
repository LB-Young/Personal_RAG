from personal_rag.config import RAG_Config
from personal_rag.rag.rank_step.rerank_client import RerankClient


class RankBlock:
    def __init__(self, query_entity):
        self.rerank_client = RerankClient()
        pass

    def ado_rank(self, query_entity):
        if RAG_Config["rank_method"] == "no_rank":
            query_entity.rank_slices = query_entity.retrival_slices
        else:
            query_entity.rank_slices = self.rerank_client.do_rerank(query_entity)
        return query_entity