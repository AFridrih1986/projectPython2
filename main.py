# from random import randint
# from time import sleep
#
# from parser_avito.parser import my_request, headers
#
#
# def main():
#     with open('files/links.txt', 'r') as file:
#         adv_urls = file.read().splitlines()
#
#     for adv_url in adv_urls:
#         try:
#             my_request(adv_url, headers=headers)
#             sleep(randint(7, 14))
#         except Exception as ex:
#             continue
#
import urllib
from urllib import parse

if __name__ == '__main__':
    # main()

    r = parse.urlparse('https://www.avito.ru/volgogradskaya_oblast/predlozheniya_uslug/transport_perevozki/spetstekhnika-ASgBAgICAkSYC8SfAZoL3J8B?p=5')
    params = urllib.parse.parse_qs(r.query)
    print(params)
