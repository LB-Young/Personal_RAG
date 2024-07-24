import json
from personal_rag.rag.retrival_step.retrival_from_local_json import RetrivalFromLocalJson

class RetrivalBlock:
    def __init__(self, query_entity):
        self.retrival_source = RetrivalFromLocalJson(query_entity)

    def ado_retrival(self, query_entity):
        query_entity = self.retrival_source.ado(query_entity)
        return query_entity