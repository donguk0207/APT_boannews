from bs4 import BeautifulSoup
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import certifi
import datetime

# SSL 인증서 검증 경고 무시
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# 뉴스 크롤링 클래스 정의
class NewsScraper:
    def __init__(self):
        self.options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
        self.options.add_experimental_option("prefs", {"safebrowsing.enabled": True})
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--start-maximized")
        self.options.add_argument('user-agent=' + user_agent)
        self.driver = webdriver.Chrome('chromedriver', options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_news_articles(self, encoded_keyword):
        url = f"https://www.boannews.com/search/news_total.asp?search=title&find={encoded_keyword}"
        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        news_list = soup.select('#news_area .news_list')

        articles = []

        for news_item in news_list:
            title_element = news_item.select_one('.news_list .news_txt')  # Selecting the title element
            title = title_element.text.strip()  # Extracting and cleaning up the title text

            content_element = news_item.select_one('.news_list .news_content')  # Selecting the title element
            content = content_element.text.strip()  # Extracting and cleaning up the title text

            link_element = title_element.find_parent('a')  # Finding the parent 'a' tag for the link
            link = link_element['href']  # Extracting the 'href' attribute from the link

            #date = news_item.select_one('.news_writer > span').text  # Extracting the date

            article = {
                '제목': title,
                '내용': content,
                'Link': 'https://www.boannews.com/'+link,
            #    'date': date
            }
            articles.append(article)

        return articles

if __name__ == "__main__":
#----------------------------------------------#
# 변경할 부분
    keyword = ""
#----------------------------------------------#
    encoded_keyword = urllib.parse.quote(keyword.encode('euc-kr'))
    scraper = NewsScraper()
    articles = scraper.scrape_news_articles(encoded_keyword)
    for article in articles:
        print(f"제목: {article['제목']}\n내용: {article['내용']}\nLink: {article['Link']}\n")