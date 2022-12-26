import time
from datetime import datetime, timedelta
import os.path


# Сохраняет время работы программы с промежутком SAVE_GAP
# и таймаутом между попытками сохранения SAVE_TIMEOUT
# Восстанавливает время работы программы из файла.
# При удалении файла, сбрасывает таймер
class Saver:
    def __init__(self, save_gap, save_timeout, filename):
        self.cur_time = datetime.now()
        self.wait_time = datetime.now()
        self.save_gap = save_gap
        self.filename = filename
        self.save_timeout = save_timeout
        self.initial_time = datetime.now()

        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                str_delta = file.read()
                t = datetime.strptime(str_delta, "%H:%M:%S")
                delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
                self.initial_time -= delta
        else:
            with open(self.filename, "w") as file:
                file.write(str(self.wait_time - self.initial_time).split(".")[0])
                print("initial save state")

    def save_state(self):
        while True:
            self.cur_time = datetime.now()
            while True:
                if not os.path.exists(self.filename):
                    self.initial_time = datetime.now() - timedelta(seconds=self.save_gap)
                self.wait_time = datetime.now()
                delta = self.wait_time - self.cur_time
                if delta >= timedelta(seconds=self.save_gap):
                    with open(self.filename, "w") as file:
                        file.write(str(self.wait_time - self.initial_time).split(".")[0])
                        print("save state")
                    break
                time.sleep(self.save_timeout)


if __name__ == "__main__":
    # seconds
    SAVE_GAP = 10
    # seconds
    SAVE_TIMEOUT = 5
    FILENAME = "state.txt"
    s = Saver(SAVE_GAP, SAVE_TIMEOUT, FILENAME)
    s.save_state()
