import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://nepalitimes.com/news')

# keywords
keywords = ['women', 'empowerment','Marginalization','madhesi','nepal']

# check status code for response received
# success code - 200
print(r)

# List to store data
data = []

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
#  print(soup.prettify())

# Getting the content tag
s = soup.find('div', class_='main--left')

# Check articles in hero
hero_article = s.find('article', class_='hero')
if hero_article:
    # Extract article details
    title = s.find("h2", class_="hero__hdl")
    description = s.find("p", class_="hero__lead")
    url = s.find("a", href=lambda x: x and x.startswith("/news"))
# Check for other articles in a href & Extract article details
url = s.find_all("a", href=lambda x: x and x.startswith("/news"))
print(url)
title2 = s.find_all("h3", class_="list__hdl")
print(title2)
author = s.find_all('span', class_='list__author')
print(author)
description2 = s.find_all("p")
i = title.text.strip()
j = description.text.strip()
d = description2
if any(keyword in title or keyword in description for keyword in keywords):
    title.lower()
    description.lower()
    data.append({"Title": title, "Content": description, "URL": url})


# author.text.strip()

# if any(keyword in title or keyword in description for keyword in keywords):
   # title.lower()
   # description.lower()
# data.append({"Title": title, "Author": author, "Content": description, "URL": url})

print(i)
print(j)
print(d)

"""url = s.find_all('a', href=True)
article_parent = s.find_all('article', class_="list")
for article in article_parent:
    article_content = s.find_all('div', class_="list__text")
    if article_content:
        title = s.find_all('h3', class_='list__hd1')
        author = s.find_all('span', class_='list__author')
        description = s.find_all('p')
        title.append(title.text)
        description.append(description.text)
        author.append(author.text)
        url.append(url.text)
    

print(article_content)"""
# news_articles = soup.find_all("article", class_="list")
    