import requests
from bs4 import BeautifulSoup
import csv

# Making a GET request to the website
url = 'https://nepalitimes.com/news'
r = requests.get(url)

# Check if the request was successful
if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article', class_='list-item')
    
    # List to store the scraped data
    data = []

    # Keywords related to women
    keywords = ['women', 'woman', 'women\'s', 'female', 'gender']

    for article in articles:
        # Extract article details
        title = article.find("h3", class_="list__hdl")
        author = article.find('span', class_='list__author')
        date = article.find('span', class_='list__date')
        description = article.find("p")

        if title and author and date and description:
            title_text = title.text.strip()
            author_text = author.text.strip()
            date_text = date.text.strip()
            description_text = description.text.strip()

            # Check if the article is related to women using keywords
            if any(keyword in title_text.lower() or keyword in description_text.lower() for keyword in keywords):
                data.append({"Title": title_text, "Author": author_text, "Date": date_text, "Content": description_text})

    # Save the data to a CSV file
    csv_file = 'women_articles.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Title", "Author", "Date", "Content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article_data in data:
            writer.writerow(article_data)

    print(f"{len(data)} articles related to women have been scraped and saved to {csv_file}.")
else:
    print(f"Failed to retrieve data from {url}. Status Code: {r.status_code}")
