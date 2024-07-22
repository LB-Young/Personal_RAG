from FlagEmbedding import FlagReranker


class BGERerank:
    def __init__(self, model_path):
        self.rerank_model = FlagReranker(model_path)

    def ado_rerank(self, query, slice_list):
        slice_query_pairs = [[query, slice] for slice in slice_list]
        scores = self.rerank_model.compute_score(slice_query_pairs)
        if len(slice_list) == 1:
            return [scores]
        else:
            return scores