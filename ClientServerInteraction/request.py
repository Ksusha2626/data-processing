import json
from pprint import pprint

import requests

VK_URL = 'https://api.vk.com/method/gifts.get'

response = requests.get(VK_URL, params={"access_token": "token", "v": "5.131"})
pprint(response.json())

with open("response.json", 'w') as f:
    f.write(json.dumps(json.loads(response.text), indent=4))
