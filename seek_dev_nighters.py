from pytz import timezone
import requests
from datetime import datetime, time
import json


def load_attempts(pages=10):
    url = 'http://devman.org/api/challenges/solution_attempts'
    try:
        for page in range(1, pages + 1):
            params = {'page': page}
            devman_data = requests.get(
                url, params=params).json()
            for record in devman_data['records']:
                yield record

    except json.decoder.JSONDecodeError:
        return None


def get_midnighters(record):
    start_time = 0
    finish_time = 6
    time_midnighters = 0
    if record['timestamp']:
        local_time = datetime.fromtimestamp(
            record['timestamp'],
            timezone(record['timezone'])
        )
        time_midnighters = local_time.time()
    if start_time < time_midnighters.hour < finish_time:
        return True


if __name__ == '__main__':
    midnighters = set()
    for record in load_attempts():
        if get_midnighters(record):
            midnighters.add(record['username'])
            print('\n '.join(midnighters))
