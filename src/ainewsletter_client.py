import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from logger import LOG

class AINewsletterClient:
    def __init__(self):
        self.url = 'https://www.ainewsletter.com/'

    def fetch_latest_articles(self):
        LOG.debug("Fetching latest AI Newsletter articles.")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            articles = self.parse_articles(response.text)
            return articles
        except Exception as e:
            LOG.error(f"Failed to fetch AI Newsletter articles: {str(e)}")
            return []

    def parse_articles(self, html_content):
        LOG.debug("Parsing AI Newsletter HTML content.")
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article')  # Adjust the selector based on actual HTML structure

        latest_articles = []
        for article in articles:
            title_tag = article.find('h2')
            link_tag = article.find('a')
            if title_tag and link_tag:
                title = title_tag.text
                link = link_tag['href']
                latest_articles.append({'title': title, 'link': link})

        LOG.info(f"Successfully parsed {len(latest_articles)} AI Newsletter articles.")
        return latest_articles

    def export_latest_articles(self):
        LOG.debug("Exporting latest AI Newsletter articles.")
        articles = self.fetch_latest_articles()

        if not articles:
            LOG.warning("No AI Newsletter articles found.")
            return None

        date = datetime.now().strftime('%Y-%m-%d')
        dir_path = os.path.join('ainewsletter', date)
        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, 'latest.md')
        with open(file_path, 'w') as file:
            file.write(f"# AI Newsletter Articles ({date})\n\n")
            for idx, article in enumerate(articles, start=1):
                file.write(f"{idx}. [{article['title']}]({article['link']})\n")

        LOG.info(f"AI Newsletter articles file generated: {file_path}")
        return file_path