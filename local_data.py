import json
import os
from datetime import datetime

"""
The important functions here are get_user_data(), which gives you the user's name and status, and log_input(), which records the input locally.
"""

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


def get_name_from_id(ids: list[str], names: list[str], user_id: str) -> str | None:
    length = len(ids)
    for i in range(length):
        if ids[i] == user_id:
            return str(names[i])

    return None


def get_ids_from_name(ids: list[str], names: list[str], name: str) -> list[str]:
    length = len(names)
    ids_list = list[str]()
    for i in range(length):
        if names[i] == name:
            ids_list.append(ids[i])

    return ids_list


def get_ids_from_id(user_id: str) -> tuple[str | None, list[str] | None]:
    """
    Returns the name of the user, and a list of all their ids.  Returns None for both if the id is not recorded.
    """
    data = get_json_file_data("names_and_ids")
    ids = data['ids']
    names = data['names']

    name = get_name_from_id(ids, names, user_id)
    if name is None:
        return None, None
    else:
        return name, get_ids_from_name(ids, names, name)


def count_id_occurrences(file_name: str, ids: list[str]) -> int:
    data = get_json_file_data(file_name)
    count = 0
    for e in data["ids"]:
        if e in ids:
            count += 1

    return count


def get_user_data(user_id: str) -> tuple[str | None, bool | None]:

    """
    Returns a tuple with the name of the user (or None if the user doesn't exist) and whether the user is signed in (or None if the user doesn't exist).
    """
    name, ids = get_ids_from_id(user_id)
    if name is None:
        return None, None
    else:
        count = (count_id_occurrences("rfid_input", ids)
                 + count_id_occurrences("form_input", ids))

        return name, count % 2 == 1


def log_input(user_id: str):
    data = get_json_file_data("new_logs")

    ids = data["ids"]
    times = data["times"]

    ids.append(user_id)
    times.append(str(datetime.now()))

    new_data = {"times": times, "ids": ids}

    write_json_data_to_file(new_data, "new_logs")


def clear_new_logs():
    write_json_data_to_file({"times": [], "ids": []}, "new_logs")



def test_data():

    log_input("broken")

    name, signed_in = get_user_data("1")
    print(f"Name: {name}")
    print(f"signed_in: {signed_in}")

