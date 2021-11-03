from reader import get_latest_url, get_news_in_page


n = get_news_in_page(get_latest_url())
print(n)