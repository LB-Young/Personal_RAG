from personal_rag.rag.utils.entities import ResponseEntity
from personal_rag.rag.retrival_step.retrival_handler import RetrivalBlock
from personal_rag.rag.rank_step.rank_handler import RankBlock
from personal_rag.rag.LLM_step.llm_handler import LLMBlock


class RAG_Handler:
    def __init__(self, query_entity):
        self.query_entity = query_entity
        self.retrivalblock = RetrivalBlock()
        self.rankblock = RankBlock()
        self.llmblock = LLMBlock()
        self.answer_entity = ResponseEntity()

    def ado(self):
        self.query_entity = self.retrivalblock.ado_retrival(self.query_entity)
        self.query_entity = self.rankblock.ado_rank(self.query_entity)
        self.query_entity = self.llmblock.ado_llm(self.query_entity)
        self.answer_entity.set_answer(self.query_entity.answer)
        return self.answer_entity