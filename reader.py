import requests
from bs4 import BeautifulSoup

from News import News


def get_latest_url():
    doc = requests.get('https://www.iiscattaneomilano.edu.it/?page_id=4414')
    doc.raise_for_status()

    soup = BeautifulSoup(doc.text, 'html.parser')
    e = soup.select_one('#post-4414 > div > p:nth-child(3)')
    return e.a['href']


def get_news_in_page(url, until=None):
    news = []
    doc = requests.get(url)
    doc.raise_for_status()

    soup = BeautifulSoup(doc.text, 'html.parser')
    entries = soup.find('div', class_='postentry')
    for x in entries.find_all('tr')[1:]:
        tds = x.find_all('td')
        n = News(
                int(tds[1].text),
                tds[0].text,
                tds[2].text,
                tds[3].a['href'],
                tds[4].a['href'] if tds[4].a is not None else None)
        if n.id == until:
            break
        news.append(n)
    return news