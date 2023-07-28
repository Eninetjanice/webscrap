import csv
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import sqlite3
import time
from urllib.parse import urljoin  # Import the urljoin function

def is_article_url(url):
    # Function to check if the URL points to an article page
    return any(keyword in url.lower() for keyword in ['article', 'story', 'news', 'feature'])

def is_relevant_article(article_content, topics_keywords):
    # Function to check if the article content contains any of the topics keywords
    return any(keyword in article_content.lower() for keyword in topics_keywords)

def scrape_articles(homepage_url, topics_keywords, start_page=1, end_page=None):
    # Step 1: Initialize the list to store all relevant articles
    articles_data = []

    # Step 2: Set of crawled URLs to avoid duplicates and infinite loops
    crawled_urls = set()

    # Step 3: Initialize the queue with the homepage URL
    queue = [(homepage_url, 0)]

    # Step 4: Convert the keywords to lowercase for case-insensitive matching
    topics_keywords = [keyword.lower() for keyword in topics_keywords]

    # Step 5: Initialize page counter
    page_count = 0

    # Step 6: Set user agent for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    while queue:
        current_url, depth = queue.pop(0)

        if current_url in crawled_urls:
            continue

        # Step 7: Fetch the page with a delay
        time.sleep(1)  # Add a delay of 1 second between requests
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Step 8: Extract relevant article links from the page
        article_links = []
        for link in soup.find_all('a', href=True):
            article_links.append(link['href'])

        # Step 9: Filter relevant articles based on topics or keywords
        relevant_article_links = []
        for link in article_links:
            if any(keyword in link.lower() for keyword in ['article', 'story', 'news', 'feature']):
                relevant_article_links.append(link)

        # Step 10: Scrape content from relevant article links
        for article_url in relevant_article_links:
            full_article_url = urljoin(current_url, article_url)

            # Check if the page number is within the desired range
            page_count += 1
            if (end_page is not None and page_count > end_page) or page_count < start_page:
                continue

            # Skip processing if the URL is not a valid webpage link or not an article page
            if not full_article_url.startswith(("http://", "https://")) or not is_article_url(full_article_url):
                continue

            try:
                # Fetch article page and extract the complete article using the newspaper library
                article = Article(full_article_url)
                article.download()
                article.parse()

                # Check if the article content contains any of the topics keywords
                if is_relevant_article(article.text, topics_keywords):
                    # Store the extracted data in a dictionary
                    article_data = {
                        'title': article.title,
                        'url': full_article_url,
                        'content': article.text,
                        'author': article.authors,
                        'publish_date': article.publish_date
                    }

                    articles_data.append(article_data)

            except requests.exceptions.SSLError as e:
                print(f"SSL Error while processing {full_article_url}: {str(e)}")
                continue

            except Exception as e:
                print(f"Error while processing {full_article_url}: {str(e)}")
                continue

        # Mark the current URL as crawled
        crawled_urls.add(current_url)

        # Step 11: Find and enqueue links to other pages
        for link in soup.find_all('a', href=True):
            link_url = urljoin(current_url, link['href'])
            if link_url not in crawled_urls and link_url.startswith(homepage_url):
                queue.append((link_url, depth + 1))

    return articles_data


if __name__ == "__main__":
    homepage_url = "https://www.firstpost.com/tag/women-empowerment"
    #homepage_url = "https://kathmandupost.com/national/2022/02/21/khas-arya-women-are-de-facto-women-leaders"
    keywords = ['women', 'empowerment','Marginalization','madhesi','nepal']
    start_page = 1  # Set the starting page number (inclusive)
    end_page = None  # Set the ending page number (exclusive) - Set None for scraping until the last page
    scraped_articles = scrape_articles(homepage_url, keywords, start_page=start_page, end_page=end_page)

    if scraped_articles:
        # Print the scraped article details
        for article in scraped_articles:
            print("Title:", article['title'])
            print("URL:", article['url'])
            print("Content:", article['content'])
            print("Author:", ", ".join(article['author']))
            print("Publish Date:", article['publish_date'])
            print("----")

        # Create database and save the articles
        create_database()
        save_to_database(scraped_articles)
        print("Articles saved to database.")
    else:
        print("No relevant articles found.")