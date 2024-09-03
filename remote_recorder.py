from threading import Thread
from time import sleep

from remote_data import RemoteData


def saver(saving):
    remote = RemoteData()
    while True:
        print("Syncing...")
        saving["val"] = True
        remote.load_remote_data()
        remote.save_new_logs_to_remote()
        saving["val"] = False
        print("Done syncing")

        sleep(10)


def start_saving(saving):
    saver_thread = Thread(target=saver, args=[saving])
    saver_thread.daemon = True
    saver_thread.start()






