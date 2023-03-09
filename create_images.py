# Importing all necessary libraries
import cv2
import os


def convert_videos_to_images(input_path, name_prefix, output_path, resize=224, to_pass=4):
    currentframe = 0

    cur_pass = 0

    for filename in os.listdir(input_path):
        if filename[-3:] != 'mp4':
            continue
        print(filename)
        cam = cv2.VideoCapture(f'{input_path}/{filename}')
        while True:
            ret, frame = cam.read()
            if ret:
                cur_pass += 1

                if cur_pass < to_pass:
                    continue
                cur_pass = 0

                # if video is still left continue creating images
                name = output_path + "/" + name_prefix + str(currentframe) + '.jpg'
                print('Creating...' + name)

                frame = cv2.resize(frame, (resize, resize))
                # writing the extracted images
                cv2.imwrite(name, frame)

                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                cam.release()
                break


convert_videos_to_images("./tired", "tired", "./images/tired", 224)
convert_videos_to_images("./awake", "awake", "./images/awake", 224)

# Release all space and windows once done
cv2.destroyAllWindows()
