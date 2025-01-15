from personal_rag.rag.utils.entities import ResponseEntity
from personal_rag.rag.retrival_step.retrival_handler import RetrivalBlock
from personal_rag.rag.rank_step.rank_handler import RankBlock
from personal_rag.rag.LLM_step.llm_handler import LLMBlock
from personal_rag.rag.self_reflection.reflection_handler import ReflectionBlock
from personal_rag.config import RAG_Config


class RAG_Handler:
    def __init__(self, query_entity):
        self.query_entity = query_entity
        self.retrivalblock = RetrivalBlock(query_entity)
        self.rankblock = RankBlock(query_entity)
        self.llmblock = LLMBlock(query_entity)
        if RAG_Config['if_use_reflection']:
            self.reflectionblock = ReflectionBlock(query_entity)
        self.answer_entity = ResponseEntity(query_entity)

    def ado(self, retrival=False):
        self.query_entity = self.retrivalblock.ado_retrival(self.query_entity)
        self.query_entity = self.rankblock.ado_rank(self.query_entity)
        if retrival:
            answer = ""
            for slice in self.query_entity.rank_slices:
                answer += "《" + slice['file_name'] + "》：" + slice['slice_content'] + "\n"
            self.answer_entity.set_answer(answer)
            return self.answer_entity
        self.query_entity = self.llmblock.ado_llm(self.query_entity)
        if RAG_Config['if_use_reflection']:
            self.query_entity = self.reflectionblock.ado_reflection(self.query_entity)
        self.answer_entity.set_answer(self.query_entity.answer)
        return self.answer_entity