from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.chosun.com/" # 조선일보 뉴스

class ChosunCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver

    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"flex-chain__column flex-chain__column-1 | box--bg-undefined grid__col--sm-8 grid__col--md-8 grid__col--lg-8 box--margin-right-md"})
        datas = []
        
        for item in root:
            link = item.find("a")
            link_url = link.get('href')
        
            datas.append(BASE_URL + link_url) 
        
        return datas
    
    # 상세 내용
    def detail(self, url):
        detail_url = url
        
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')

        title = detail_soup.find("h1", {"class":"article-header__headline | font--primary text--black"}).text # 제목
        writer = detail_soup.find("a", {"class":"article-byline__author | text--wrap-pre text--black text__link--underline"}).text #작성자
        content = detail_soup.find("section" , {"class" : "article-body"}).text # 본문

        dates =detail_soup.find_all("span", {"class" : "font--size-sm-14 font--size-md-14 text--grey-60"})
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일


        return [title, detail_url, writer, reg_date, content]