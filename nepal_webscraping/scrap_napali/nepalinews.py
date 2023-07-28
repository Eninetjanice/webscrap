import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

def scrape_website_for_keywords(url, keywords):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles_data = []

    # Find all <article> elements with the class "hero"
    hero_articles = soup.find_all("article", class_="hero")

    for article in hero_articles:
        # Extract article details
        title = article.find("h2", class_="hero__hdl").text.strip()
        content = article.find("p", class_="hero__lead").text.strip()
        url = article.find("a", href=True)["href"]
        new_url = urljoin(url, url)  # Resolve relative URL to absolute URL

        # Check if the article contains the specified keywords
        if any(keyword.lower() in content.lower() for keyword in keywords):
            # Find the author and date elements
            info_div = article.find("div", class_="article__info")
            author_element = info_div.find("span", class_="article__author")
            date_element = info_div.find("time", class_="article__time")

            # Extract the author and date if they exist
            author = author_element.text.strip() if author_element else None
            date = date_element["datetime"].split()[0] if date_element else None

            articles_data.append({
                "Title": title,
                "Content": content,
                "URL": url,
                "Author": author,
                "Date": date
            })

    # Find all <a> elements with an href attribute starting with "/news"
    anchor_articles = soup.find_all("a", href=lambda x: x and x.startswith("/news"))

    for anchor_article in anchor_articles:
        # Find the <article class="list"> element within the <a> element
        article = anchor_article.find("article", class_="list")

        if article:
            # Find the title of the article within the <article class="list"> element
            title_element = article.find("h3", class_="list__hdl")
            title = title_element.text.strip() if title_element else None

            # Find the content of the article
            content_element = article.find("p")
            content = content_element.text.strip() if content_element else None

            # Find the author and date of publication
            author_and_date_element = article.find("span", class_="list__author")
            author_and_date = author_and_date_element.text.strip() if author_and_date_element else None
            if author_and_date and " in " in author_and_date:
                author, date = author_and_date.split(" in ")
            else:
                author, date = None, None

            # Find the URL of the article
            full_url = urljoin(url, anchor_article["href"])

            # Check if any of the keywords are present in the title or content
            if any(keyword in title.lower() or keyword in content.lower() for keyword in keywords):
                articles_data.append({"Title": title, "Content": content, "Author": author, "Date": date, "URL": full_url})

    return articles_data

def main():
    url = "https://nepalitimes.com/news"
    keywords = ['women', 'girl', 'empowerment', 'Marginalization', 'madhesi', 'nepal']
    articles_data = scrape_website_for_keywords(url, keywords)

    # Save the data to a CSV file
    with open("articles_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Content", "URL", "Author", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article_data in articles_data:
            writer.writerow(article_data)

if __name__ == "__main__":
    main()
