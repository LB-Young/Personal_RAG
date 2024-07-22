import os
import json


from personal_rag.document_split.extractor_handler import ExtractorHandler
from personal_rag.document_split.utils.get_filepath_list import get_file_path_list


class DocumentExtractor:
    def __init__(self, file_path):
        self.ext = None
        self.file_path_list = get_file_path_list(file_path)
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
        self.all_slices = all_slices
        self.save_slices()
        return all_slices
    
    def save_slices(self):
        with open("F:\Cmodels\Personal_RAG\personal_rag\slice_database\slices.json", "w", encoding="utf-8") as f:
            json.dump(self.all_slices, f, ensure_ascii=False, indent=4)
        return
    
