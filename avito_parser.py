import datetime
import random

import requests
import bs4
import pandas as pd
import urllib
import installations
import time
import fake_useragent
from random import randint
from dataclasses import dataclass


@dataclass
class Advertisement:
    title: str = ''
    price: str = ''
    date: str = ''
    phone: str = ''
    company: str = ''
    contact: str = ''
    number: str = ''
    views: str = ''
    address: str = ''
    description: str = ''


headers = [
    {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        },

    {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
]


def my_request(url, headers, retry=5):
    try:
        user = fake_useragent.UserAgent().random
        headers['user-agent'] = user
        session = requests.Session()
        response = session.get(url, headers=headers)
        response.raise_for_status()
        print(f'{url} => {response.status_code}')

    except Exception as e:
        print(e)
        if retry:
            print(f'[INFO]: retry={retry} => {url}')
            time.sleep(randint(60, 60*2))
            my_request(url, retry=(retry-1))
        else:
            with open('files/notparse.txt', 'a') as file:
                file.write(url + '\n')
            raise
    else:
        return response


def main():
    with open('files/links.txt', 'r') as file:
        adv_urls = file.read().splitlines()

    for adv_url in adv_urls:
        try:
            my_request(adv_url, headers=headers[0])
            time.sleep(randint(7, 14))
        except Exception as ex:
            continue


if __name__ == '__main__':
    main()
        