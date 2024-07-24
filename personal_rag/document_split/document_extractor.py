import os
import json

from personal_rag.document_split.extractor_handler import ExtractorHandler
from personal_rag.document_split.utils.get_filepath_list import get_file_path_list
from personal_rag.document_split.embedding.embedding_client import EmbeddingClient
from personal_rag.slice_database.chroma_database.chromadb_client import ChromadbClient


class DocumentExtractor:
    def __init__(self, file_path, need_embedding, db_name, db_type="local"):
        self.ext = None
        self.file_path = file_path
        self.need_embedding = need_embedding
        self.db_name = db_name
        self.db_type = db_type
        if self.need_embedding:
            self.embedding_client = EmbeddingClient()
        else:
            self.db_type = "local"
        if self.db_type == "chromadb":
            self.chromadb_client = ChromadbClient()
        self.file_path_list = get_file_path_list(self.file_path)
        self.all_slices = None

    def do_extract(self):
        all_slices = {}
        for file_path in self.file_path_list:
            ext = file_path.split(".")[-1]
            if "\\" in file_path:
                file_name = "".join(file_path.split("\\")[-1].split(".")[:-1])
            else:
                file_name = "".join(file_path.split("/")[-1].split(".")[:-1])
            cur_slices = ExtractorHandler(file_path, ext).do_extract()
            for slice in cur_slices:
                slice['file_name'] = file_name
            all_slices[file_name] = cur_slices
        if self.need_embedding:
            self.all_slices = self.embedding_client.do_embedding(all_slices)
        else:
            self.all_slices = all_slices
        if self.db_type == "local":
            self.save_slices_to_local_file()
        elif self.db_type == "chromadb":
            self.save_to_chromadb()
        else:
            self.save_slices_to_local_file()
        return all_slices
    
    def save_slices_to_local_file(self):
        with open(f"F:/Cmodels/Personal_RAG/personal_rag/slice_database/local_database/{self.db_name}.json", "w", encoding="utf-8") as f:
            json.dump(self.all_slices, f, ensure_ascii=False, indent=4)
        print(f"slice save to 'F:/Cmodels/Personal_RAG/personal_rag/slice_database/local_database/{self.db_name}.json'")
        return
    
    def save_to_chromadb(self):
        res = self.chromadb_client.collection_add_slice(self.db_name, self.all_slices)
        print(res)