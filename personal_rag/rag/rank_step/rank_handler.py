

class RankBlock:
    def __init__(self):
        pass

    def ado_rank(self, query_entity):
        query_entity.rank_slices = query_entity.retrival_slices
        return query_entity