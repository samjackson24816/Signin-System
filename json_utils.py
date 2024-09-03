import json
import os


def get_json_file_data(file_name: str) -> dict | None:
    path = f"./data/{file_name}.json"
    if not os.path.exists(path):
        print(f"WARNING: Asked to open a json file named {file_name}, which doesn't exist")
        return None
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json_data_to_file(data: dict, file_name: str):
    path = f"./data/{file_name}.json"
    if not os.path.exists(path):
        print(f"WARNING: Asked to write to open a json file named {file_name}, which doesn't exist")
        return
    f = open(path, 'w')
    new_json = json.dumps(data, indent=4)
    f.write(new_json)
    f.close()
