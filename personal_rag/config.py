DocumentSplit_Config = {
    "embedding_model_path": "F:\Cmodels\Personal_RAG\personal_rag\model_weights\m3e_base",
    "device":"cpu"
}

RAG_Config = {
    "device":"cpu",
    "slice_rank_method":["jac","cos"],
    "rank_method":"bge_rerank",
    "rerank_model_path":"F:/Cmodels/Personal_RAG/personal_rag/model_weights/bge_rerank/AI-ModelScope/bge-reranker-v2-m3"
}