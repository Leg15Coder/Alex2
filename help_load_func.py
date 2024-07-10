import json
import numpy as np
from functions import *
"""
d = {
    'get_info_by_ip': [(norm("Найди"), norm("IP")), (norm("Отследи"), norm("IP"))],
    'open_browser': [(norm("зайди"), norm("браузер")), (norm("зайди"), norm("гугл")), (norm("открой"), norm("гугл")),
                     (norm("открой"), norm("браузер"))],
    'join_vk': [(norm("зайди"), norm("ВК")), (norm("зайди"), norm("Вконтакте"))],
    'scroll_vk_news': [(norm("Полистай"), norm("Ленту"))],
    'gcd': [(norm("Найди"), norm("делитель"))],
    'find_top_nouns': [(norm("проанализируй"), norm("текст"))],
    'full_lexeme_of_word': [(norm("просклоняй"), norm("слово"))]
}
print(d)
with open("memory/functions.json", 'w', encoding='utf-8') as f:
    json.dump(d, f)
with open("memory/functions.json", 'r', encoding='utf-8') as f:
    print(json.load(f))
"""
s = str()
with open("D:\Dima\Projects\Labmedia_faces\models\withTeacherModel_arrays1.txt", 'r') as f:
    labels = list()
    images = list()
    while s != 'end.':
        s = f.readline().replace('\n', '')
        if s == 'end.':
            break
        labels.append(int(s.split()[1]))
        images.append([])
        for _ in range(int(s.split()[0])):
            s = int(f.readline().replace('\n', ''))
            images[-1].append(list(map(int, f.readline().replace('\n', '').split())))
        # images[-1] = np.array(images[-1], 'uint8')
d = dict()
for l, i in zip(labels, images):
    if l in d:
        d[l].append(i)
    else:
        d[l] = [i]
with open("memory/people_faces_memory.json", 'w') as f:
    json.dump(d, f)
d = dict()

"""
data = self.people_faces_memory
        print(0)
        while True:  # cv2.waitKey(1) != ord('q'):
            print(1)
            _, image = self.eyes.read()
            print(2)
            locations = face_recognition.face_locations(image, model="cnn")
            print(2.5)
            encodings = face_recognition.face_encodings(image, locations)
            print(3, locations, encodings)
            for face_encoding, face_location in zip(encodings, locations):
                result = face_recognition.compare_faces(data["encodings"], face_encoding)
                print(4)
                if True in result:
                    match = data["name"], data["status"]
                else:
                    match = "НЕОПОЗНАНО", "НЕОПОЗНАНО"
                top, right, bottom, left = face_location
                cv2.rectangle(image, (left, top), (right, bottom), color[match[1]], 4)
                cv2.rectangle(image, (left, top), (right, bottom + 24), color[match[1]], cv2.FILLED)
                cv2.putText(
                    image, match[0],
                    (left + 10, bottom + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 3
                )
            cv2.imshow("eyes", image)
        self.eyes.release()
        cv2.destroyAllWindows()
"""
"""
                if self.people_faces_memory is not None:
                    number_predicted, conf = self.people_faces_memory.predict(black_white[y: y + height, x: x + width])
                    color = colors[self.facedict[number_predicted]["status"]]
                    cv2.putText(frame, self.facedict[number_predicted]["name"], (x, y-5),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                else:
                    """
