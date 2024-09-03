import json
import os
from datetime import datetime
from json_utils import *

"""
The important functions here are get_user_data(), which gives you the user's name and status, and log_input(), which records the input locally.
"""


def get_name_from_id(names_and_ids: list[list[str, str]], user_id: str) -> str | None:
    length = len(names_and_ids)
    for i in range(length):
        if names_and_ids[i][0] == user_id:
            return str(names_and_ids[i][1])

    return None


def get_ids_from_name(names_and_ids: list[list[str, str]], name: str) -> list[str]:
    length = len(names_and_ids)
    ids_list = list[str]()

    for i in range(length):
        if str(names_and_ids[i][1]) == name:
            ids_list.append(names_and_ids[i][0])

    return ids_list


def get_ids_from_id(user_id: str) -> tuple[str | None, list[str] | None]:
    """
    Returns the name of the user, and a list of all their ids.  Returns None for both if the id is not recorded.
    """
    data = get_json_file_data("names_and_ids")
    names_and_ids = data["names_and_ids"]

    name = get_name_from_id(names_and_ids, user_id)
    if name is None:
        return None, None
    else:
        return name, get_ids_from_name(names_and_ids, name)


def count_id_occurrences(file_name: str, ids: list[str]) -> int:
    data = get_json_file_data(file_name)
    count = 0
    for e in data[file_name]:
        if str(e[0]) in ids:
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

    # Append the input the local copy of rfid_input so we have an immediate record of it
    rfid_data = get_json_file_data("rfid_input")
    rfid_input = rfid_data["rfid_input"]
    rfid_input.append([user_id])
    new_rfid_data = {"rfid_input": rfid_input}
    write_json_data_to_file(new_rfid_data, "rfid_input")

    data = get_json_file_data("new_logs")
    times_and_ids = data["times_and_ids"]
    times_and_ids.append([str(datetime.now()), user_id])
    new_data = {"times_and_ids": times_and_ids}
    write_json_data_to_file(new_data, "new_logs")


def clear_new_logs():
    write_json_data_to_file({"times_and_ids": [[]]}, "new_logs")


def test_data():
    clear_new_logs()

    for e in ["1", "1", "1", "9644", "1"]:
        log_input(e)
        name, signed_in = get_user_data(e)
        print(f"Name: {name}")
        print(f"signed_in: {signed_in}")
