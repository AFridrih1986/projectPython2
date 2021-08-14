import requests, bs4

res = requests.get('https://kg-portal.ru/movie/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'lxml')
p = soup.select('p')
print(type(p))

print(len(p))
print(p[0].attrs)
