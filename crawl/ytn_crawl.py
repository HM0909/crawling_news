from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.ytn.co.kr/" # YTN 뉴스

class YtnCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver


    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
    
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"now01 YTN_CSA_bottomnews1"}) 
        items = root.find_all("ul")  
        datas = []
        
        for item in items:
            data = item.find("li")
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

        top = detail_soup.find("div", {"class":"top"})
        title = top.find("h3").text #제목
        
        writer = ""
        
        orgin_content = detail_soup.find("div" , {"class" : "article"})
            
        writers = str(orgin_content).split('<br/>')
        real_writer = ""
        
        for writer in writers:
            if writer.find('@ytn.co.kr') > 0:
                real_writer = writer 
                
        section = detail_soup.find("div" , {"class" : "article"})
        content = section.find("span").text #본문
            
        dates =detail_soup.find_all("span", {"class" : "time"})
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

        return [title, detail_url, writer, reg_date, content]
