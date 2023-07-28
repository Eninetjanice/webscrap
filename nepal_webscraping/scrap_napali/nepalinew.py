import requests
from bs4 import BeautifulSoup
import csv


def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find("div", class_="main--left")
    link = data.find_all('a', href=True)
    for link in link:
        ['href']
    links = [link['href'] for link in data.find_all('a', href=True)]
    print(links)
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        # Write the data to the CSV file
        writer.writerow({'URL': links})


def scrape_website_by_keyword(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article')

    for article in articles:
        # Check if the keyword is present in the article
            if keyword.lower() in article.get_text().lower():
                # Extract author, content, and date of publication
                author = article.find('span', class_='author').get_text() if article.find('span', class_='author') else "Unknown Author"
                content = article.find('div', class_='content').get_text() if article.find('div', class_='content') else "Content not available."
                date = article.find('span', class_='date').get_text() if article.find('span', class_='date') else "Unknown Date"
                with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
                    fieldnames = ['Author', 'Date', 'Content']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    # Write the data to the CSV file
                    writer.writerow({'Author': author, 'Date': date, 'Content': content})

if __name__ == "__main__":
    root = "https://nepalitimes.com"
    url = f'{root}/news'
    keyword_to_search = "women"
    output_csv_file = "scraped_data.csv"
    scrape_website_by_keyword(url, keyword_to_search)
    get_url(root)
