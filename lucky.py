import bs4, requests, webbrowser

query = input('Введите запрос: ')
res = requests.get('https://google.com/search?q=' + query)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')

link_elems = soup.select('a')

# print(link_elems)

num_open = min(10, len(link_elems))
for ls in range(num_open):
    webbrowser.open('https://google.com' + link_elems[ls].get('href'))
    # print(type(ls))


#  python programming tutorials