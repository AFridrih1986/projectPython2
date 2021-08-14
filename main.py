import requests


res = requests.get('https://gutenberg.org/cache/epub/1112/pg1112.txt')

res.raise_for_status()
play_file = open('test.txt', 'wb')
for chunk in res.iter_content(10000):
    play_file.write(chunk)

play_file.close()
