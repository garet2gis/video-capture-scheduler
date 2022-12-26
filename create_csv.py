import cv2
import mediapipe as mp
import numpy as np
import math
import csv
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
# cap = cv2.VideoCapture('./tired/2022-12-25 23:44:59.873050.mp4')

right_eye = [[33, 133], [160, 144], [159, 145], [158, 153]]  # right eye landmark positions
left_eye = [[263, 362], [387, 373], [386, 374], [385, 380]]  # left eye landmark positions
mouth = [[61, 291], [39, 181], [0, 17], [269, 405]]  # mouth landmark coordinates


def distance(p1, p2):
    return (((p1[:2] - p2[:2]) ** 2).sum()) ** 0.5


def eye_aspect_ratio(landmarks, eye):
    N1 = distance(landmarks[eye[1][0]], landmarks[eye[1][1]])
    N2 = distance(landmarks[eye[2][0]], landmarks[eye[2][1]])
    N3 = distance(landmarks[eye[3][0]], landmarks[eye[3][1]])
    D = distance(landmarks[eye[0][0]], landmarks[eye[0][1]])
    return (N1 + N2 + N3) / (3 * D)


def eye_feature(landmarks):
    return (eye_aspect_ratio(landmarks, left_eye) + eye_aspect_ratio(landmarks, right_eye)) / 2


def mouth_feature(landmarks):
    N1 = distance(landmarks[mouth[1][0]], landmarks[mouth[1][1]])
    N2 = distance(landmarks[mouth[2][0]], landmarks[mouth[2][1]])
    N3 = distance(landmarks[mouth[3][0]], landmarks[mouth[3][1]])
    D = distance(landmarks[mouth[0][0]], landmarks[mouth[0][1]])
    return (N1 + N2 + N3) / (3 * D)


def perimeter(landmarks, eye):
    return distance(landmarks[eye[0][0]], landmarks[eye[1][0]]) + \
           distance(landmarks[eye[1][0]], landmarks[eye[2][0]]) + \
           distance(landmarks[eye[2][0]], landmarks[eye[3][0]]) + \
           distance(landmarks[eye[3][0]], landmarks[eye[0][1]]) + \
           distance(landmarks[eye[0][1]], landmarks[eye[3][1]]) + \
           distance(landmarks[eye[3][1]], landmarks[eye[2][1]]) + \
           distance(landmarks[eye[2][1]], landmarks[eye[1][1]]) + \
           distance(landmarks[eye[1][1]], landmarks[eye[0][0]])


def perimeter_feature(landmarks):
    return (perimeter(landmarks, left_eye) + perimeter(landmarks, right_eye)) / 2


def area_eye(landmarks, eye):
    return math.pi * ((distance(landmarks[eye[1][0]], landmarks[eye[3][1]]) * 0.5) ** 2)


def area_mouth_feature(landmarks):
    return math.pi * ((distance(landmarks[mouth[1][0]], landmarks[mouth[3][1]]) * 0.5) ** 2)


def area_eye_feature(landmarks):
    return (area_eye(landmarks, left_eye) + area_eye(landmarks, right_eye)) / 2


def pupil_circularity(landmarks, eye):
    return (4 * math.pi * area_eye(landmarks, eye)) / (perimeter(landmarks, eye) ** 2)


def pupil_feature(landmarks):
    return (pupil_circularity(landmarks, left_eye) +
            pupil_circularity(landmarks, right_eye)) / 2


def get_features(video_path):
    cap = cv2.VideoCapture(video_path)
    features = []
    frame_count = 0

    pass_frame = False

    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            if frame_count == 221:
                break

            if pass_frame:
                pass_frame = False
                continue
            pass_frame = True

            success, image = cap.read()

            if not success:
                break
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                landmarks_positions = []
                # assume that only face is present in the image
                for _, data_point in enumerate(results.multi_face_landmarks[0].landmark):
                    landmarks_positions.append(
                        [data_point.x, data_point.y, data_point.z])  # saving normalized landmark positions

                landmarks_positions = np.array(landmarks_positions)
                landmarks_positions[:, 0] *= image.shape[1]
                landmarks_positions[:, 1] *= image.shape[0]

                eye = eye_feature(landmarks_positions)
                mouth = mouth_feature(landmarks_positions)
                area_eye = area_eye_feature(landmarks_positions)
                area_mouth = area_mouth_feature(landmarks_positions)
                pupil = pupil_feature(landmarks_positions)

                features.append([frame_count, eye, mouth, area_eye, area_mouth, pupil])
                frame_count += 1

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()

    return features


header = ['frame_count', 'eye', 'mouth', 'area_eye', 'area_mouth', 'pupil', 'label']

with open('data.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for filename in os.listdir("tired"):
        if filename[-3:] != 'mp4':
            continue
        print(filename)
        features = get_features(f'./tired/{filename}')
        for row in features:
            # write the row
            writer.writerow([*row, 1])

    for filename in os.listdir("awake"):
        if filename[-3:] != 'mp4':
            continue
        print(filename)
        features = get_features(f'./awake/{filename}')

        for row in features:
            # write the row
            writer.writerow([*row, 0])
