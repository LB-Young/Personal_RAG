import requests
import cohere
from personal_rag.config import get_api_key


class CohereRerank:
    def __init__(self):
        api_key = get_api_key("cohere")
        self.co = cohere.ClientV2(api_key = api_key)

    def ado_rerank(self, query, slice_list):

        response = self.co.rerank(
            model="rerank-v3.5",
            query=query,
            documents=slice_list,
            top_n=len(slice_list),
        )
        scores_result = response.results
        sorted_result = sorted(scores_result, key=lambda x: x.index, reverse=True)

        scores = [item.relevance_score for item in sorted_result]
        return scores


