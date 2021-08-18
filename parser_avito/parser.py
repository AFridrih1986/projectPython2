import csv
from datetime import datetime
from datetime import timedelta
import random
import time
from collections import namedtuple
from urllib import parse
import requests
import bs4

InnerBlock = namedtuple('Block', 'title,price,currency,date,url')


class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.price}\t{self.currency}\t{self.date}\t{self.url}'


class AvitoParser:
    _headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    def __init__(self, url: str = None, page: int = None, radius: int = 0, user: int = 0, retry: int = 5):
        self.domain = 'https://www.avito.ru'
        self.session = requests.Session()

        self.session.headers = AvitoParser._headers

        self.url = url
        self.retry = retry
        self.page = self.__get_page(page=page, radius=radius, user=user, retry=self.retry)
        self.label_get_page = False

    def __get_page(self, retry, page: int = None, radius: int = 0, user: int = 0):
        params = {
            'radius': radius,
            'user': user
        }

        if page and page > 0:
            params['p'] = page
        try:
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            print(f'{self.url} => {response.status_code}')
            time.sleep(random.randint(7, 14))
        except Exception as e:
            print(e)
            if retry:
                print(f'[INFO]: retry={retry} => {self.url}')
                time.sleep(random.randint(60, 60 * 2))
                self.__get_page(retry=(retry - 1))
            else:
                with open('../files/notparse.txt', 'a') as file:
                    file.write(self.url + '\n')
                raise
        else:
            self.page = response.text
            return self.page

    def parse_date(self, item: str):
        mark_minute = ['минут', 'минута', 'минуты']
        mark_hour = ['час', 'часов', 'часа']

        mark_day = ['дня', 'день', 'дней']
        mark_week = ['неделю', 'недели', 'недель']
        params = item.strip().split(' ')
        params = [p.strip() for p in params]
        # print(type(params))

        if len(params) == 2:
            day, time = params
            if day == 'Сегодня':
                date = datetime.today()
            elif day == 'Вчера':
                date = datetime.today() - timedelta(days=1)
            else:
                print('Не смогли разобрать какой день: ', item)
                return
            time = datetime.strptime(time, '%H:%M').time()
            return datetime.combine(date=date, time=time).strftime("%y-%m-%d %H:%M")

        elif len(params) == 3:
            if any((mark_minute[0] in params, mark_minute[1] in params, mark_minute[2] in params)):
                minute = int(params[0])
                today = datetime.now()
                date = today - timedelta(minutes=minute)
                return date.strftime("%y-%m-%d %H:%M")

            elif any((mark_hour[0] in params, mark_hour[1] in params, mark_hour[2] in params)):

                hour = int(params[0])
                today = datetime.now()
                date = today - timedelta(hours=hour)
                return date.strftime("%y-%m-%d %H:%M")

            elif any((mark_day[0] in params, mark_day[1] in params, mark_day[2] in params)):
                day = int(params[0])
                today = datetime.now()
                date = today - timedelta(days=day)
                return date.strftime("%y-%m-%d %H:%M")

            elif any((mark_week[0] in params, mark_week[1] in params, mark_week[2] in params)):
                week = int(params[0])
                today = datetime.now()
                date = today - timedelta(days=week * 7)
                return date.strftime("%y-%m-%d %H:%M")
            else:
                day, month_hru, time = params
                day = int(day)
                months_map = {
                    'января': 1,
                    'февраля': 2,
                    'марта': 3,
                    'апреля': 4,
                    'мая': 5,
                    'июня': 6,
                    'июля': 7,
                    'августа': 8,
                    'сентября': 9,
                    'октября': 10,
                    'ноября': 11,
                    'декабря': 12
                }
                month = months_map.get(month_hru)
                if not month:
                    print('Не смогли разобрать месяц: ', item)
                    return
                today = datetime.today()
                time = datetime.strptime(time, '%H:%M').time()
                return datetime(day=day, month=month,
                                year=today.year,
                                hour=time.hour,
                                minute=time.minute).strftime("%y-%m-%d %H:%M")

    def parse_block(self, item):
        # извлечь блок с ссылкой
        url_block = item.select_one('a.title-root_maxHeight-3obWc')
        href = url_block.get('href')
        if href:
            url = self.domain + href
        else:
            url = None

        # извлечь блок с названием
        title_block = item.select_one('div.iva-item-titleStep-2bjuh h3.text-bold-3R9dt')
        title = title_block.string.strip()

        # извлечь блок с ценой
        price_block = item.select_one('span.price-text-1HrJ_')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
        else:
            price, currency = 'Цена не указана', ''

        # извлечь блок с датой
        date = None
        date_block = item.select_one('div.date-root-3w7Ry')
        date_block = date_block.select_one('.date-text-2jSvU')
        absolute_date = date_block.get_text()
        if absolute_date:
            date = self.parse_date(absolute_date)

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date
        )

    def get_pagination_limit(self):
        soup = bs4.BeautifulSoup(self.page, 'lxml')
        container = soup.select('a.pagination-page')
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1
        r = parse.urlparse(href)
        params = parse.parse_qs(r.query)
        return int(params['p'][0])

    def get_blocks(self, page: int = None, radius: int = 0, user: int = 0):
        if self.label_get_page:
            html_page = self.__get_page(self.retry)
        else:
            self.label_get_page = True
            html_page = self.page

        list_blocks = []
        soup = bs4.BeautifulSoup(html_page, 'lxml')
        container = soup.select('div.iva-item-content-m2FiN')
        for item in container:
            block = self.parse_block(item)
            list_blocks.append(block)
            print(block)
        return list_blocks

    def parse_all(self):
        list_all_blocks = []
        limit = self.get_pagination_limit()
        print(limit)

        for i in range(1, limit + 1):
            list_all_blocks.extend(self.get_blocks(page=i))

        return list_all_blocks


if __name__ == '__main__':
    avito = AvitoParser(
        url='https://www.avito.ru/ivanovo/predlozheniya_uslug/transport_perevozki/spetstekhnika-ASgBAgICAkSYC8SfAZoL3J8B?',
        user=2)

    list_all = avito.parse_all()
    print(len(list_all))

    with open('../files/poster.csv', 'a', newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        for ls in list_all:
            writer.writerow([ls.title,
                             ls.price.replace('\xa0', ''),
                             ls.currency,
                             ls.date,
                             ls.url])
