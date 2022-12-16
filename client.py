import json
import sys
import requests
from time import sleep


def get_profile(user_id: int):
    _res = requests.get(f'http://127.0.0.1:8000/{user_id}')
    return _res.text


while True:
    res = get_profile(sys.argv[1])  # NOQA
    response = json.loads(res)
    name = response['name']
    print(f'Hello {name}')
    sleep(float(sys.argv[2]))

