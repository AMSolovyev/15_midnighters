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
            total_pages = devman_data['number_of_pages']
            if params == total_pages:
                break

    except json.decoder.JSONDecodeError:
        return None


def is_midnighter(attempt):
    start_time = 0
    finish_time = 6
    time_midnighters = 0
    if attempt['timestamp']:
        time_midnighters = datetime.fromtimestamp(
            attempt['timestamp'],
            timezone(attempt['timezone'])
        )
    return start_time < time_midnighters.hour < finish_time


if __name__ == '__main__':
    midnighters = set()
    for record in load_attempts():
        if is_midnighter(record):
            midnighters.add(record['username'])
    print('\n '.join(midnighters))
