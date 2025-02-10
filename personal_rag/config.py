DocumentSplit_Config = {
    "embedding_mode": "aliyun",
    "embedding_remote_url": "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding",
    "embedding_model_name": "multimodal-embedding-v1",
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
    with open(file="/Users/liubaoyang/Documents/windows/api_key.json",mode="r", encoding="utf-8") as f:
        config = json.load(f)
        return config[platform]
    