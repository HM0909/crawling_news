from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101" # naver 뉴스
ROOT_URL = "https://news.naver.com"

class NaverCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
       
        
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"section_body"})
        items = root.find_all("dl")
        datas = []

        for item in items:
            data = item.find("dt") 
            link = data.find("a")
            link_url = link.get('href')
            
            datas.append(link_url) 
        
        return datas


    # 상세 내용
    def detail(self, url):
        detail_url = url
    
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')
        
        title = detail_soup.find("div", {"class" : "media_end_head_title"}).text #제목
        
        writer = ""
        if detail_soup.find("div", {"class" : "media_end_head_journalist"}) != None:
            writer = detail_soup.find("div", {"class" : "media_end_head_journalist"}).text #작성자
        
        content = detail_soup.find("div", {"class" : "go_trans _article_content"}).text #본문
    
        all_date =detail_soup.find("div" , {"class" : "media_end_head_info_datestamp"})
        dates =all_date.find_all("div")
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

          
        return [title, detail_url, writer, reg_date, content]