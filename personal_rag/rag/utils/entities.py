class QueryEntity:
    def __init__(self):
        self.query = ""
        self.retrival_slices = []
        self.rank_slices = []
        self.prompt = ""
        self.temperature = 1.0
        self.answer = ""

    def requests_param_extract(self, requests_params):
        self.query = requests_params.query
        self.temperature = requests_params.temperature
        return


class ResponseEntity:
    def __init__(self):
        self.answer = ""

    def set_answer(self, answer):
        self.answer = answer