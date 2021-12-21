from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://www.hani.co.kr" #한겨레 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw2.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw2.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"main-top01"})
    items = root.find_all("div", {"class":"article-area"})
    datas = []
    
    for item in items:
        data = item.find("h4", {"class":"article-title"}) 
        link = data.find("a")
        link_url = link.get('href')
        
        datas.append(detail(base_url + link_url))

    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(CSV_FILE_PATH, datas, CSV_HEADER)
             
       
#상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    
    title = detail_soup.find("span", {"class" : "title"}).text #제목
    writer = ""
    
    if detail_soup.find("div", {"class" : "name"}) != None:
       writer = detail_soup.find("div", {"class" : "name"}).text #작성자
    
    section = detail_soup.find("div" , {"class" : "article-text-font-size"})
    content = section.find("div" , {"class" : "text"}).text #본문
    
    
    all_date =detail_soup.find("p" , {"class" : "date-time"})
    dates =all_date.find_all("span")
    
    if len(dates) > 1:
        reg_date = dates[1].text  # 수정일
    else:
        reg_date = dates[0].text  # 입력일

            
    return [title, writer, reg_date, content]
 

def main(): 
    driver.get(base_url)
    
    crawling()

    driver.quit()
    
if __name__ == '__main__':
    main()