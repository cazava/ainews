import logging

import requests
import json

import config

API_KEY = config.API_KEY
class Writer:
    def __init__(self):

        self.url = "https://api.theb.ai/v1/chat/completions"
        # url = "https://api.baizhi.ai/v1/chat/completions"

        self.API_KEY = config.API_KEY

    def get_post(self, text_post: str):
        messages = [
            {
                "role": "user",
                "content": f"Переведи текст с английского на русский и перепиши, как будто делаешь обзор на сервис, в ответе должен быть только обзор. {text_post}"
            }
        ]
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": messages,
            "stream": False
        })
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", self.url, headers=headers, data=payload)
            content = response.json()['choices'][0].get('message').get('content')
            return content
        except:
            logging.error('Requset AI error')


def prices(file):
    with open(file, "r") as f:
        res = {}
        data = json.load(f)
        for model in data['data']:
            res[(f'{model.get("id")}')] = (model.get("pricing").get('input'))
    min_value = min(res.values())
    min_key = [key for key, value in res.items() if value == min_value]
    print(f'min_value: {min_value}, min_key: {min_key}')


def ai_list():
    url = "https://api.theb.ai/v1/models"
    # url = "https://api.baizhi.ai/v1/models"
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.json())
    with open('list.json', "w") as file:
        json.dump(response.json(), file, indent=4)
