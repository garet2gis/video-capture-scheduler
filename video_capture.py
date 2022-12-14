from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import time
from datetime import datetime
from popup import init_popup
import shutil
from config import RESOLUTION, FRAMERATE, TIME

options = {
    "CAP_PROP_FRAME_WIDTH": RESOLUTION,
    "CAP_PROP_FRAME_HEIGHT": RESOLUTION,
    "CAP_PROP_FPS": FRAMERATE,
}

output_params = {}


def start_shoot():
    stream = VideoGear(source=0, logging=True, **options).start()

    filename = f"{datetime.now()}.mp4"

    writer = WriteGear(output_filename=filename, logging=True, **output_params)

    start = time.perf_counter()
    while True:
        frame = stream.read()

        if frame is None:
            break

        writer.write(frame)

        stop = time.perf_counter()
        if stop - start > TIME:
            break

    stream.stop()
    writer.close()

    # копируем видео в нужную папку
    shutil.move(filename, init_popup())


if __name__ == "__main__":
    start_shoot()
