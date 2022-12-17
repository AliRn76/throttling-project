import json
import sys
import requests
from time import sleep

if len(sys.argv) < 3:
    print('You Should pass "UserID" & "SleepTime" Args\nExample: python client.py 1 0.2')
    exit()

USER_ID = sys.argv[1]
SLEEP_TIME = float(sys.argv[2])


def get_profile(user_id: int) -> tuple[int, dict]:
    _res = requests.get(f'http://127.0.0.1:8000/{user_id}')
    return _res.status_code, json.loads(_res.text)


def main():
    while True:
        status_code, response = get_profile(USER_ID)  # NOQA
        if status_code == 200:
            name = response['name']
            print(f'StatusCode: {status_code} | Hello {name}')
        else:
            print(f'StatusCode: {status_code} | {response["detail"]}')
        sleep(SLEEP_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
