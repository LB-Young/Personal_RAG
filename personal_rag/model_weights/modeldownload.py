#模型下载
from modelscope import snapshot_download
# model_dir = snapshot_download('Jerry0/m3e-base', cache_dir="F:/Cmodels/Personal_RAG/personal_rag/model_weights/m3e_base", revision='master')
# print(model_dir)


model_dir = snapshot_download('AI-ModelScope/bge-reranker-v2-m3', cache_dir="F:/Cmodels/Personal_RAG/personal_rag/model_weights/bge_rerank", revision='master')
print(model_dir)