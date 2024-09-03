from threading import Thread
from time import sleep

from remote_data import RemoteData


def saver(saving):
    remote = RemoteData()
    while True:
        print("Syncing...")
        saving["val"] = True
        remote.save_new_logs_to_remote()
        remote.load_remote_data()
        saving["val"] = False
        print("Done syncing")

        sleep(20)


def start_saving(saving):
    saver_thread = Thread(target=saver, args=[saving])
    saver_thread.daemon = True
    saver_thread.start()






