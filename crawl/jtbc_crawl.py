from crawl_manager import *
from bs4 import BeautifulSoup as bs
import utils.string_util as string_util

BASE_URL = "https://news.jtbc.joins.com/section/list.aspx?scode=" # JTBC 뉴스
ROOT_URL = "https://news.jtbc.joins.com"

class JtbcCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
       
        
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
    
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("ul", {"id":"section_list"})
        items = root.find_all("li")
        datas = []

        for item in items:
            data = item.find("dt", {"class":"title_cr"})
            link = data.find("a")
            link_url = link.get("href")
                
            datas.append(ROOT_URL + link_url)  
        
        return datas


    # 상세 내용
    def detail(self, url):
        detail_url = url
    
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')
        
        title = detail_soup.find("h3", {"id" : "jtbcBody"}).text #제목
        
        writer = ""
    
        if detail_soup.find("dd", {"class" : "name"}) != None:
            writer = detail_soup.find("dd", {"class" : "name"}).text #작성자
            
        content = string_util.relace_tag(detail_soup.find("div", {"class" : "article_content"}).text) #본문
        
        all_date =detail_soup.find("span" , {"class" : "artical_date"})
        dates =all_date.find_all("span")
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일


        return [title, detail_url, writer, reg_date, content]