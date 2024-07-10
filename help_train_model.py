import os
import pickle
import sys
import face_recognition
from cv2 import cv2


def train_model_by_img():
    known_encodings, data = list(), dict()
    catalog = [f for f in os.listdir("datasets") if os.path.isdir(f)]
    for f_name in catalog:
        folder = os.listdir(f"datasets/{f_name}")
        for file in folder:
            face_img = face_recognition.load_image_file(f"datasets/{f_name}/{file}")
            face_enc = face_recognition.face_encodings(face_img)[0]
            if len(known_encodings) == 0:
                known_encodings.append(face_enc)
            else:
                for item in range(0, len(known_encodings)):
                    result = face_recognition.compare_faces([face_enc], known_encodings[item])
                    if result[0]:
                        known_encodings.append(face_enc)
        data[f_name] = known_encodings
    with open("memory/people_faces_memory.pickle", "wb") as file:
        file.write(pickle.dumps(data))
        print(data)
    return f"[INFO] File successfully created"


train_model_by_img()
