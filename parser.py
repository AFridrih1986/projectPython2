import datetime
import random

import requests, bs4
import pandas as pd
import urllib
import installations
import time
import fake_useragent
from random import randint
from dataclasses import dataclass
import parce_phone


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


def get_list_of_links(path_file):
    set_links = set()
    try:
        with pd.ExcelFile(path_file) as exel:
            df = pd.read_excel(exel, sheet_name='Лист1')

            for d in df['Unnamed: 1'].dropna():
                set_links.add(urllib.parse.unquote(d))
    except Exception as e:
        print(e)

    return list(set_links)


def get_html(url):
    try:
        user = fake_useragent.UserAgent().random
        header = {'user-agent': user, 'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7'}
        print(header)
        session = requests.Session()
        session.headers = header
        res = session.get(url, headers=header)

        res.raise_for_status()
        print('Выполнено!!!!!')

    except Exception as e:
        print('Ошибка!!!!', e)

        print('HEADER________', res.headers)
        time.sleep(random.randint(1, 30))
        user = fake_useragent.UserAgent().random
        header = {'user-agent': user}
        res = requests.get(url, headers=header)

    return res.text


def get_total_pages(html):
    try:
        total_pages = 0
        soup = bs4.BeautifulSoup(html, 'lxml')
        pages = soup.find('div', {'class': 'pagination-pages'}).find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = urllib.parse.unquote(pages).rpartition('p=')[-1].partition('&')[0]
        print(pages, '\t', total_pages)

    except Exception as e:
        total_pages = 0
        print(e)
    return int(total_pages)


def get_list_url_pages(url):
    # Разбираем и декодируем https запрос

    url_page = urllib.parse.urlparse(urllib.parse.unquote(url))
    qr = 'q='
    pg = 'p='

    total_pages = get_total_pages(get_html(url_page.geturl()))
    list_pages = []

    for n_page in range(1, total_pages + 1):
        if qr in url_page.query:
            in_qr = url_page.query.find(qr)
            url_page = url_page._replace(query=pg + str(n_page) + '&' + url_page.query[in_qr:])

        else:
            url_page = url_page._replace(query=pg + str(n_page))

        list_pages.append(url_page.geturl())

    return list_pages


def get_list_link_advertisement(url):
    try:
        list_link_advertisement = []
        domen = 'https://www.avito.ru'

        user = fake_useragent.UserAgent().random
        header = {'user-agent': user}

        res = requests.get(url, headers=header)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')
        pages_advertisement = soup.find_all(lambda tag: tag.name == 'div' and \
                                                        tag.get('class') == ['iva-item-titleStep-2bjuh'])

        for ls in pages_advertisement:
            list_link_advertisement.append(domen + ls.find(lambda tag: tag.name == 'a').get('href'))

    except Exception as e:
        print(e)
    return list_link_advertisement


def get_advertisement(url_advertisement):
    try:
        user = fake_useragent.UserAgent().random
        header = {'user-agent': user}

        res = requests.get(url_advertisement, headers=header)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')
        advertisement = Advertisement()

        advertisement.title = soup.find(lambda tag: tag.name == 'span' \
                                                    and tag.get('class') == ['title-info-title-text']).text.strip()

        advertisement.price = soup.find(lambda tag: tag.name == 'div' \
                                                    and tag.get('class') == ['item-price-wrapper']).text.strip()

        advertisement.date = soup.find(lambda tag: tag.name == 'div' \
                                                   and tag.get('class') == [
                                                       'title-info-metadata-item-redesign']).text.strip()

        advertisement.company = soup.find(lambda tag: tag.name == 'div' \
                                                      and tag.get('class') == ['seller-info-col']).text.replace('\n','')

        advertisement.contact = soup.find(lambda tag: tag.name == 'div' \
                                                      and tag.get('class') == ['seller-info-label']) \
            .find_next_sibling('div', class_='seller-info-value').text.strip()

        view_search = advertisement.company = soup.find(lambda tag: tag.name == 'div' \
                                                                    and tag.get('class') == [
                                                                        'item-view-search-info-redesign']).text.split()

        advertisement.number = view_search[1]
        advertisement.views = str(int(view_search[3]) + int(view_search[4].replace('(+', '').replace(')', '')))

        advertisement.address = soup.find(lambda tag: tag.name == 'span' \
                                                      and tag.get('class') == ['item-address__string']).text.strip()

        advertisement.description = soup.find(lambda tag: tag.name == 'div' \
                                                          and tag.get('class') == [
                                                              'item-description-text']).text.strip()

        advertisement.phone = parce_phone.Bot().number_phone
        print(advertisement.phone)
    except Exception as e:
        print(e)

    return advertisement


list_link_in_exel = get_list_of_links(installations.file_excel)
all_link_list_write = []

for ls in list_link_in_exel:
    all_link_list_write.extend(get_list_url_pages(ls))
    time.sleep(randint(1, 20))

list_link_advertisement = get_list_link_advertisement(all_link_list_write[0])
advertisement = get_advertisement(list_link_advertisement[0])

print(advertisement.title)
print(advertisement.price)
print(advertisement.date)
print(advertisement.phone)
print(advertisement.company)
print(advertisement.contact)
print(advertisement.number)
print(advertisement.views)
print(advertisement.address)
print(advertisement.description)


