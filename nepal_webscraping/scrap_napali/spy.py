import requests
from bs4 import BeautifulSoup


parent_url = 'https://nepalitimes.com/'
''' other_urls = [parent_url + '/news', parent_url + '/multimedia', parent_url + '/editorial',
              parent_url + '/features', parent_url + '/review', parent_url + '/archive',
              parent_url + '/opinion', parent_url + '/business']'''
req = requests.get(parent_url)
req_content = req.text
soup = BeautifulSoup(req_content, 'lxml')

news = soup.find('div', class_='main--left')
articles = news.a['href']
print(articles)

'''for article in articles:
    article_url = articles["href"]
    print(article_url)
    description = news.find('p').text.replace(' ', '')
    title = news.find('h3', class_='')
   
    # more_info = news.find('a', href=True)
    if /news not in more_info:

    if keyword in description or any(keyword) in title:
       authour = news.find('span', class_='list__author').span.text.replace'''
