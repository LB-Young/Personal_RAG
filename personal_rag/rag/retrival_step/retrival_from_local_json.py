import json
import numpy as np
from personal_rag.config import RAG_Config
from personal_rag.other_models.embedding import BGEEmbedding


class RetrivalFromLocalJson:
    def __init__(self, query_entity):
        self.embedding_client = BGEEmbedding()
        with open(f"F:\Cmodels\Personal_RAG\personal_rag\slice_database\local_database\{query_entity.db_name}.json", "r", encoding="utf-8") as f:
            self.database = json.load(f)
        self.all_slices = []
        for key, value in self.database.items():
            for slice in value:
                slice['name_slice_content'] = "《" + key + "》" + slice['slice_content']
                self.all_slices.append(slice)

    def ado(self, query_entity):
        query = query_entity.query
        embedding_response = self.embedding_client.do_embedding([query])
        query_embedding = embedding_response[0]
        for index, slice in enumerate(self.all_slices):
            jac_score, cos_score = 0, 0
            if "jac" in RAG_Config['slice_rank_method']:
                jac_score = self.cal_jac_similarity(query, slice['name_slice_content'])
            if "cos" in RAG_Config['slice_rank_method']:
                cos_score = self.cal_cos_similarity(query_embedding, slice['embedding'])
            slice['retrival_similarity'] = 0.3*jac_score + cos_score
        self.all_slices.sort(key=lambda x:x['retrival_similarity'], reverse=True)
        top_slices = min(10, len(self.all_slices))
        tmp_retrival_slices = self.all_slices[:top_slices]
        all_retrival_slices = tmp_retrival_slices
        get_all_next_slices = []
        for slice in tmp_retrival_slices:
            get_all_next_slices.extend(slice['subordinate_ids'])
        for slice in self.all_slices[top_slices:]:
            if slice['id'] in get_all_next_slices:
                all_retrival_slices.append(slice)
        query_entity.retrival_slices = all_retrival_slices
        return query_entity

    def cal_jac_similarity(self, query, slice_content):
        slice_set = set(slice_content)
        query_set = set(query)
        jaccard_score = len(slice_set & query_set) / len(query_set)
        return jaccard_score
    
    def cal_cos_similarity(self, query_embedding, slice_embeddings):
        vec1 = np.array(query_embedding)
        vec2 = np.array(slice_embeddings)
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        cosine_sim = dot_product / (norm_vec1 * norm_vec2)
        return cosine_sim
