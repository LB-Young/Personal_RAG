class QueryEntity:
    def __init__(self):
        self.query = ""
        self.retrival_slices = []
        self.rank_slices = []
        self.prompt = ""
        self.temperature = 1.0
        self.answer = ""
        self.db_name = "tmp"
        self.need_embedding = False
        self.db_type = "local"

    def requests_param_extract(self, requests_params):
        self.query = requests_params.query
        self.temperature = requests_params.temperature
        self.need_embedding = requests_params.need_embedding
        self.db_name = requests_params.db_name
        self.db_type = requests_params.db_type
        return


class ResponseEntity:
    def __init__(self, query_entity):
        self.answer = ""

    def set_answer(self, answer):
        self.answer = answer