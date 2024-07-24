from FlagEmbedding import FlagReranker
from personal_rag.config import RAG_Config

class BGERerank:
    def __init__(self):
        self.rerank_model = FlagReranker(model_name_or_path=RAG_Config['rerank_model_path'], use_fp16=True)

    def ado_rerank(self, query, slice_list):
        slice_query_pairs = [[query, slice] for slice in slice_list]
        scores = self.rerank_model.compute_score(slice_query_pairs)
        if len(slice_list) == 1:
            return [scores]
        else:
            return scores