import pyttsx3, speech_recognition, wave, json, os, asyncio, pickle, face_recognition
from vosk import Model, KaldiRecognizer
from cv2 import cv2
from PIL import Image, ImageDraw
from functions import *
import numpy as np


class VoiceAssistant:
    def __init__(self):
        self.name = "Alex"
        self.voice = pyttsx3.init()
        self.voice.setProperty("voice", self.voice.getProperty("voices")[0].id)
        self.recognizer = speech_recognition.Recognizer()
        self.ears = speech_recognition.Microphone()
        self.eyes = cv2.VideoCapture(0)
        self.modelClass = cv2.CascadeClassifier(r"models/haarcascade_frontalface_default.xml")
        self.people_faces_memory = # pickle.loads(open("memory/people_faces_memory.pickle", "rb").read())
        self.facedict = json.load(open("memory/facedict.json", 'r'))
        self.browser = None
        self.buffer = str()
        self.memory = json.load(open("memory/functions.json", 'r', encoding='utf-8'))
        # + подгрузка БД с навыками и знаниями + инициализация ИИ

    def say(self, frase):
        if not frase:
            return False
        print(self.name + ':', frase)
        self.buffer += frase + '\n'
        self.voice.say(str(frase))
        self.voice.runAndWait()
        return True

    def record(self):
        with self.ears:
            recognized_data = ""
            try:
                self.recognizer.adjust_for_ambient_noise(self.ears, duration=2)
                audio = self.recognizer.listen(self.ears, 5, 5)
                try:
                    with open("microphone-results.wav", "wb") as file:
                        file.write(audio.get_wav_data())
                except speech_recognition.WaitTimeoutError:
                    self.say("Я ничего не слышу")
                    try:
                        recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()
                    except speech_recognition.UnknownValueError:
                        self.say("Мне сложно")
                    except speech_recognition.RequestError:
                        if not os.path.exists("../../My_code/models/vosk-model-small-ru-0.4"):
                            return False
                        wave_audio_file = wave.open("microphone-results.wav", "rb")
                        model = Model("../../My_code/models/vosk-model-small-ru-0.4")
                        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())
                        data = wave_audio_file.readframes(wave_audio_file.getnframes())
                        if len(data) > 0:
                            if offline_recognizer.AcceptWaveform(data):
                                recognized_data = offline_recognizer.Result()
                                recognized_data = json.loads(recognized_data)
                                recognized_data = recognized_data["text"]
                        else:
                            self.say("Я пока не могу понять, можете перефразировать?")
            except Exception as ex:
                recognized_data = str(ex)
            return recognized_data

    def hear(self):
        voice_input = self.record()
        if os.path.exists("microphone-results.wav"):
            os.remove("microphone-results.wav")
        return voice_input

    def look(self):
        colors = {
            "НЕОПОЗНАНО": (255, 255, 0),
            "ДРУГ": (50, 255, 50),
            "ВРАГ": (250, 5, 5)
        }
        data = self.people_faces_memory
        while cv2.waitKey(1) != ord('q'):
            _, image = self.eyes.read()
            black_white = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.modelClass.detectMultiScale(black_white, scaleFactor=1.1, minNeighbors=7,
                                                     minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb, faces)
            color, name = colors["НЕОПОЗНАНО"], "НЕОПОЗНАНО"
            for encoding in encodings:
                for person in data:
                    print(data[person], encoding, sep='\n*****\n')
                    matches = face_recognition.compare_faces(data[person], encoding)
                    if True in matches:
                        name = self.facedict[person]["name"]
                        color = colors[self.facedict[person]["status"]]
                        break
            for x, y, width, height in faces:
                cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)
                cv2.putText(image, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow('Faces', image)

    def get_intent(self, text):
        data = set(map(norm, del_punctuation(text).split()))
        for intent in self.memory:
            for form in self.memory[intent]:
                s1 = set(form)
                if s1.issubset(data):
                    args = list(data - s1)
                    self.say(self.execute_command(globals()[intent], *args))
                    return True
        try:
            self.say(self.execute_command(generate_gpt, text))
        except Exception as ex2:
            self.say("Я не могу ничего ответить, " + str(ex2))
        return False

    def learn_by_text(self, text, intent=None):
        pass  # Самообучение на основе полученного текста

    def answer(self, text):
        try:
            self.get_intent(text)
        except Exception as ex:
            alex.say(str(ex))
        finally:
            answ = self.buffer[:]
            self.buffer = str()
            return answ

    def execute_command(self, command, *args, **kwargs):
        if command is open_browser:
            self.browser = open_browser()
            return "Открываю Google Chrome"
        elif command is join_vk:
            self.say("Выполняю")
            if self.browser is None:
                self.browser = open_browser()
                return command(self.browser)
            else:
                return command(self.browser)
        elif command is scroll_vk_news:
            if self.browser is None:
                self.browser = open_browser()
                join_vk(self.browser)
                return command(self.browser)
            else:
                return command(self.browser)
        else:
            return command(*args, **kwargs)


alex = VoiceAssistant()


def main():
    alex.look()


if __name__ == '__main__':
    main()
