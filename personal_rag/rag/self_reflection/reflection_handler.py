from personal_rag.config import RAG_Config


class ReflectionBlock:
    def __init__(self, query_entity):
        pass

    def ado_reflection(self, query_entity):
        query = query_entity.query
        answer = query_entity.answer
        