import random
import json
import requests


start_phrase = [
    'Привет!',
    'Как дела?',
    'Йоу, го знакомиться!!!',
    'Гулять идешь?',
    'У меня для тебя сюрприз ...',
    'Как я тебе?'
]

API = 'https://genrec.beautybooking.ml/api/getrec'


def get_first_message():
    first_msg = random.choice(start_phrase)
    if random.randint(0, 1) == 1:
        first_msg = ' '.join([first_msg, random.choice(start_phrase)])
    return first_msg


def get_answer(msg):
    query = {"text": msg}
    response = requests.post(API, json=query)
    text = json.loads(response.text)
    return text["text"][0][0]
