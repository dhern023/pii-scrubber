import json
import pathlib

def read_json_to_dict(fname):
    path_in = pathlib.Path(fname)
    with open(path_in, 'r') as file:
        data = json.load(file)
    
    return data

def lazy_load_txt(fname):
    path_in = pathlib.Path(fname)
    with open(path_in, 'r') as file:
        for line in file.readlines():
            yield line.strip()
            