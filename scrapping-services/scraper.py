import requests
from bs4 import BeautifulSoup
import re
import csv

class SkyNewsScraper:
    def __init__(self, url):
        self.url = url
        self.articles = []

    def fetch_content(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
        return response.content

    def parse_content(self, content):
        soup = BeautifulSoup(content, 'html5lib')
        h2_tags = soup.find_all('h2', class_='ui-section-header display-any font-brand-2')
        return h2_tags

    def extract_data(self, h2_tags):
        for h2 in h2_tags:
            article_info = {}
            span = h2.find('span', class_='ui-section-header-title')
            if span:
                article_info['title'] = span.get_text(strip=True)
            
            parent = h2.parent
            if parent:
                img = parent.find('img')
                if img and 'src' in img.attrs:
                    article_info['thumbnail_url'] = img['src']
                else:
                    div = parent.find('div', style=re.compile('background-image'))
                    if div:
                        style = div['style']
                        match = re.search(r'url\((.*?)\)', style)
                        if match:
                            article_info['thumbnail_url'] = match.group(1).strip('\'"')
                
                link = parent.find('a')
                if link and 'href' in link.attrs:
                    article_info['url'] = link['href']
                    if not article_info['url'].startswith('http'):
                        article_info['url'] = f"https://news.sky.com{article_info['url']}"
                
                context = parent.find('p')
                if context:
                    article_info['context'] = context.get_text(strip=True)
            
            if article_info:
                self.articles.append(article_info)

    def save_to_csv(self, file_name):
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'thumbnail_url', 'url', 'context'])
            writer.writeheader()
            writer.writerows(self.articles)
        print(f"Data has been saved to {file_name}")

    def scrape(self):
        content = self.fetch_content()
        if content:
            h2_tags = self.parse_content(content)
            self.extract_data(h2_tags)
            self.save_to_csv("sky_news_articles.csv")

if __name__ == '__main__':
    scraper = SkyNewsScraper("https://news.sky.com/")
    scraper.scrape()
    for article in scraper.articles:
        print(f"Title: {article.get('title', 'N/A')}")
        print(f"Thumbnail URL: {article.get('thumbnail_url', 'N/A')}")
        print(f"URL: {article.get('url', 'N/A')}")
        print(f"Context: {article.get('context', 'N/A')}")
        print()