DocumentSplit_Config = {
    "embedding_mode": "together",
    "embedding_remote_url": "http://10.252.242.3:8901",
    "embedding_model_path": "F:\Cmodels\model_weights\m3e_base",
    "device":"cpu"
}


RAG_Config = {
    "device":"cpu",
    "slice_rank_method":["jac","cos"],
    "rank_method":"cohere_rerank",
    "rerank_model_path":"F:/Cmodels/model_weights/bge_rerank/AI-ModelScope/bge-reranker-v2-m3",
    "if_use_reflection":False,
    "merge_type":"all"
}

import json

def get_api_key(platform):
    with open(file=r"C:\Users\86187\Desktop\api_key.json",mode="r", encoding="utf-8") as f:
        config = json.load(f)
        return config[platform]
    