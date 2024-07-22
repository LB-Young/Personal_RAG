import json



class RetrivalFromLocalJson:
    def __init__(self):
        with open("F:\Cmodels\Personal_RAG\personal_rag\slice_database\slices.json", "r", encoding="utf-8") as f:
            self.database = json.load(f)
        self.all_slices = []
        for key, value in self.database.items():
            for slice in value:
                slice['name_slice_content'] = "《" + key + "》" + slice['slice_content']
                self.all_slices.append(slice)

    def ado(self, query_entity):
        query = query_entity.query
        for index, slice in enumerate(self.all_slices):
            slice['retrival_similarity'] = self.cal_similarity(query, slice['name_slice_content'])
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

    def cal_similarity(self, query, slice_content):
        slice_set = set(slice_content)
        query_set = set(query)
        jaccard_score = len(slice_set & query_set) / len(query_set)
        return jaccard_score
