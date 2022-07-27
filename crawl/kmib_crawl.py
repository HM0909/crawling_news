from crawl_manager import *
from bs4 import BeautifulSoup as bs
import utils.string_util as string_util

BASE_URL = "http://www.kmib.co.kr/news/index.asp" # 국민일보 뉴스

class KmibCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
        
        
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("dd", {"class":"rel_lst"})
        items = root.find_all("a")
        datas = []
    
        for item in items:
        
            datas.append(item.get('href'))
        
        return datas
    
    
    # 상세 내용
    def detail(self, url):
        detail_url = url
        
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')

        head = detail_soup.find("div", {"class":"nwsti"})
        title = head.find("h3").text    # 제목
        
        orgin_content = detail_soup.find("div" , {"class" : "tx"})
        str_content = str(orgin_content)
        
        writers = str(orgin_content).split('<br/>')  # 작성자
        real_writer = ""
        
        for writer in writers:
            if writer.find('@kmib.co.kr') > 0:
                real_writer = writer 
                
        content = string_util.relace_tag(str_content.replace('<br/>', '\n'))   # 본문
    
        dates = detail_soup.find_all("span" , {"class" : "t11"})
    
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

        
        return [title, detail_url, writer, reg_date, content]
