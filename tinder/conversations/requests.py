import requests 
import json

p = {"text": "Ты где?"}
r = requests.post('https://genrec.beautybooking.ml/api/getrec', json=p)

text = json.loads(r.text)

print(text["text"][0][0])