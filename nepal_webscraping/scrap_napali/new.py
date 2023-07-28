import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://nepalitimes.com/news')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
#  print(soup.prettify())

# Getting the content tag
s = soup.find('div', class_='main--left')
content = s.find_all('a', href=True)
article_parent = s.find_all('article', class_="list")
for article in article_parent:
    article_content = s.find_all('div', class_="list__text")
    if article_content:
        title = s.find_all('h3', class_='list__hd1')
        author = s.find_all('span', class_='list__author')
        content = s.find_all('p')
        

print(article_content)
 
