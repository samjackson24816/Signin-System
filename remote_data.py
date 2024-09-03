import pygsheets
from pygsheets import Worksheet, authorize

import local_data
from json_utils import *


def load_and_save_sheet_data(ws: Worksheet, start_col: str, end_col: str, name: str):
    vals = ws.get_values(start_col + "1", end_col)

    # Removing the header row
    vals.pop(0)

    json_data = {name: vals}
    write_json_data_to_file(json_data, name)


class RemoteData:

    rfid_input_ws: Worksheet
    names_and_ids_ws: Worksheet
    form_input_ws: Worksheet


    def __init__(self):

        try:
            client = authorize(service_file='service-account-key.json')
        except:
            raise "The sheet was not authorized.  This is a big problem.  Have fun with it"

        sh = client.open_by_key("13a-zji7i5hih5loJxG55xtRv_mPDe2VjCdHcyz-XXCU")
        self.rfid_input_ws = sh.worksheet_by_title("RFID Input")
        self.names_and_ids_ws = sh.worksheet_by_title("Names & IDs")
        self.form_input_ws = sh.worksheet_by_title("Form Input")

    def load_remote_data(self):
        load_and_save_sheet_data(self.names_and_ids_ws, "A", "B", "names_and_ids")
        load_and_save_sheet_data(self.rfid_input_ws, "B", "B", "rfid_input")
        load_and_save_sheet_data(self.form_input_ws, "B", "B", "form_input")

    def save_new_logs_to_remote(self):
        data = get_json_file_data("new_logs")


        local_data.clear_new_logs()


        rows = self.rfid_input_ws.rows

        new_rows = data["times_and_ids"]
        new_rows.pop(0)

        for e in new_rows:
            self.rfid_input_ws.add_rows(1)
            self.rfid_input_ws.update_values("A" + str(self.rfid_input_ws.rows), [e])



def test_remote_data():
    rd = RemoteData()

    rd.save_new_logs_to_remote()
