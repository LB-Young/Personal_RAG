DocumentSplit_Config = {
    "embedding_model_path": "F:\Cmodels\model_weights\m3e_base",
    "device":"cpu"
}

RAG_Config = {
    "device":"cpu",
    "slice_rank_method":["jac","cos"],
    "rank_method":"bge_rerank",
    "rerank_model_path":"F:/Cmodels/model_weights/bge_rerank/AI-ModelScope/bge-reranker-v2-m3",
    "if_use_reflection":True,
    "merge_type":"all"
}