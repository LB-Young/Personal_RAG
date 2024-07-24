from personal_rag.rag.LLM_step.prompt_process import slice_merge_prompt
from personal_rag.LLM_model.llm_client import LLMClient


class LLMBlock:
    def __init__(self, query_entity):
        self.llm_client = LLMClient()

    def ado_llm(self, query_entity):
        query = query_entity.query
        slices = query_entity.rank_slices
        prompt = slice_merge_prompt(query, slices)
        answer = self.llm_client.ado_requests(prompt)
        query_entity.answer = answer
        return query_entity