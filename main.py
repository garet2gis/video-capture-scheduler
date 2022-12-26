import time
import os
from datetime import datetime, timedelta
from video_capture import start_shoot
from multiprocessing import Process
from saver import Saver
from config import SAVE_TIMEOUT, SAVE_GAP, TIMEOUT, READ_TIMEOUT, FILENAME


def schedule():
    print("first start shoot video")
    start_shoot()
    while True:
        if not os.path.exists(FILENAME):
            time.sleep(READ_TIMEOUT)
            continue

        with open(FILENAME, "r") as file:
            str_delta = file.read()
            t = datetime.strptime(str_delta, "%H:%M:%S")
            delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            cur_delta = timedelta(seconds=TIMEOUT)
            if cur_delta < delta:
                print("start shoot video")
                start_shoot()
                if os.path.exists(FILENAME):
                    os.remove(FILENAME)

            time.sleep(READ_TIMEOUT)


if __name__ == "__main__":
    S = Saver(SAVE_GAP, SAVE_TIMEOUT, FILENAME)
    proc = Process(target=S.save_state, daemon=True)
    proc.start()
    schedule()
    proc.terminate()
