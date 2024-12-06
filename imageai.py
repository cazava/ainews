import requests
import json

import config

# url = "https://api.theb.ai/v1/images/generations"
url = "https://api.baizhi.ai/v1/images/generations"

payload = json.dumps({
    "model": "dall-e-2",
    "model_params": {
        "n": 2,
        "size": "256x256"
    },
    "prompt": "a funny logo for a telegram channel that talks about innovations in the field of artificial intelligence"
})
headers = {
    'Authorization': f'Bearer {config.API_KEY}',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

# Проверка статуса ответа
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
