from pytz import timezone
import requests
from datetime import datetime, time
import json


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts'
    params = {'page': 0}
    try:
        while True:
            params['page'] += 1
            devman_data = requests.get(
                url, params=params).json()
            for record in devman_data['records']:
                yield record

    except json.decoder.JSONDecodeError:
        return None


def is_midnighters(attempt):
    start_time = 0
    finish_time = 6
    time_midnighters = 0
    if attempt['timestamp']:
        local_time = datetime.fromtimestamp(
            attempt['timestamp'],
            timezone(attempt['timezone'])
        )
        time_midnighters = local_time
    return start_time < time_midnighters.hour < finish_time


if __name__ == '__main__':
    midnighters = set()
    for record in load_attempts():
        if is_midnighters(record):
            midnighters.add(record['username'])
    print('\n '.join(midnighters))
