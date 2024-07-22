import os


def get_file_path_list(file_path):
    if os.path.isfile(file_path):
        return [file_path]
    if os.path.isdir(file_path):
        all_filepath = []
        for cur_path in os.path.listdir(file_path):
            all_filepath.extend(get_file_path_list(cur_path))
        return all_filepath
    
