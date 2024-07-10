import requests, os, sys, time, random, pickle, folium, pymorphy2, openai
from pyfiglet import Figlet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import config
from aiogram.types import URLInputFile

openai.api_key = config.openai_token.get_secret_value()


class Browser:
    def __init__(self):
        user_agents_list = [
            "hello_world",
            "best_of_the_best",
            "python_today"
        ]
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f"user-agent={random.choice(user_agents_list)}")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=Service(r"../../My_code/models/chromedriver"), options=self.options)
        self.open_url("https://yandex.ru/")

    def __del__(self):
        self.driver.close()
        self.driver.quit()

    def write(self, element, text, enter=False, speed=0.1):
        element.clear()
        for key in text:
            time.sleep(speed)
            element.send_keys(key)
        time.sleep(max(0.5, 1 - speed))
        if enter:
            element.send_keys(Keys.ENTER)
            time.sleep(1)

    def open_url(self, url, max_window=False):
        self.driver.get(url)
        if max_window:
            self.driver.maximize_window()
        time.sleep(3)

    def load_cookies(self):
        time.sleep(2)
        for cookie in pickle.load(open("memory/cookies/vk_cookies", "rb")):
            self.driver.add_cookie(cookie)
        time.sleep(2)


def get_info_by_ip(ip='127.0.0.1'):
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('IP INFO'))
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region Name]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon'),
        }
        for k, v in data.items():
            print(f'{k} : {v}')
        area = folium.Map(location=[response.get('lat'), response.get('lon')])
        area.save(f'{response.get("query")}_{response.get("city")}.html')
        return "Веду сканирование IP, вот область примерного местоположения"
    except requests.exceptions.ConnectionError:
        return 'Не могу отследить, проверь подключение к интернету'


def open_browser():
    return Browser()


def join_vk(browser):
    browser.open_url("https://vk.com/", True)
    browser.write(browser.driver.find_element(By.NAME, "email"), config.my_phone.get_secret_value())
    browser.write(browser.driver.find_element(By.NAME, "pass"), config.vk_password.get_secret_value(), True)
    browser.load_cookies()
    browser.driver.refresh()


def scroll_vk_news(browser, speed=300):
    i = 0
    while True:
        browser.driver.execute_script(f"window.scroll({{ left: 0, top: {i}, behavior: 'smooth' }});")
        time.sleep(1 / speed)
        i += 1


def gcd(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            a, b = lst[i], lst[j]
            while a != b:
                if a % b == 0 or b % a == 0:
                    if a > b:
                        a -= b * (a // b - 1)
                    else:
                        b -= a * (b // a - 1)
                else:
                    if a > b:
                        a %= b
                    else:
                        b %= a
                lst[i], lst[j] = a, b
    return "Наибольший общий делитель этих чисел:" + str(lst[-1])


def norm(word):
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].normal_form


def is_istance(*args):
    if not args:
        return True
    for word in args:
        if norm(word) != norm(args[0]):
            return False
    return True


def del_punctuation(text):
    return text.replace('!', ' ').replace(';', ' ').replace('-', ' ').replace(',', ' ').replace('.', ' ') \
        .replace('?', ' ').replace(':', ' ')


def find_top_nouns(text, n=5):
    morph = pymorphy2.MorphAnalyzer()
    text = del_punctuation(text)
    d = dict()
    for word in text.split():
        if 'NOUN' in morph.parse(word)[0].tag and morph.parse(word)[0].score > 0.5:
            word = morph.parse(word)[0].normal_form
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
    lst = list()
    while len(lst) < n and len(d) > 0:
        mx = d[max(d, key=lambda x: d[x])]
        lst1 = [i for i in d if d[i] == mx]
        for i in lst1:
            del d[i]
        lst1.sort(reverse=True)
        while len(lst) < n and len(lst1) > 0:
            lst, lst1 = lst + [lst1[0]], lst1[1:]
    return str(n) + " наиболее популярных слов в данном тексте: " + ', '.join(lst)


def full_lexeme_of_word(word):
    morph = pymorphy2.MorphAnalyzer()
    flag, answ = None, "Склоняю:\n"
    for w in morph.parse(word):
        if 'NOUN' in w.tag:
            flag = 'NOUN'
            word = w
            break
        elif 'VERB' in w.tag or 'INFN' in w.tag:
            flag = 'VERB'
            word = w
            break
    if flag == 'NOUN':
        d = {0: 'Именительный падеж:', 1: 'Родительный падеж:', 2: 'Дательный падеж:', 3: 'Винительный падеж:',
             4: 'Творительный падеж:', 5: 'Предложный падеж:'}
        counter = 0
        for i in word.lexeme:
            if counter == 0:
                answ += 'Единственное число:\n'
            if counter == 6:
                answ += 'Множественное число:\n'
            print(d[counter % 6], i.word)
            counter += 1
    elif flag == 'VERB':
        answ += 'Прошедшее время:\n'
        answ += '\n'.join([i.word for i in word.lexeme[7:11]])
        answ += 'Настоящее время:'
        answ += '\n'.join([i.word for i in word.lexeme[1:7]])
    else:
        answ = 'Не могу ответить'
    return answ


def generate_password(m):
    res = str()
    for i in range(m):
        elem = random.choice(symb)
        while elem in res:
            elem = random.choice(symb)
        res += elem
    usl = (set(string.ascii_uppercase) & set(res)) and (set(string.ascii_lowercase) & set(res))
    usl = usl and (set(string.digits) & set(res))
    if usl:
        return "Можете попробовать такой пароль: " + res
    return generate_password(m)


def generate_gpt(text):
    response_chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response_chat['choices'][0]['message']['content']


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]
    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    return result


def generate_image(prompt):
    # await message.answer("Генерируем ответ, это может занять несколько секунд")
    response_img = openai.Image.create(
        prompt=prompt,
        n=1,
        size='512x512',
        response_format='b64_json'
    )
    image = b64decode(response_img['data'][0]['b64_json'])
    name = '_'.join(prompt.split())
    with open(f"images/{name}.png", 'wb') as f:
        f.write(image)
        return f
