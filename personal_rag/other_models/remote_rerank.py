import requests

class RemoteRerank:
    def __init__(self):
        self.base_url = ""

    def ado_rerank(self, query, slice_list):
        slice_query_pairs = [[query, slice] for slice in slice_list]
        scores = requests.post(self.base_url,slice_query_pairs)
        if len(slice_list) == 1:
            return [scores]
        else:
            return scores
