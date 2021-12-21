from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://www.mbn.co.kr/pages/news/index.html" # MBN 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw5.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw5.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"list_news"})
    items = root.find_all("li")
    datas = []
    
    for item in items:
        link = item.find("a")
        link_url = link.get('href')
        
        datas.append(detail(link_url))
    
    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(CSV_FILE_PATH, datas, CSV_HEADER)
             
             
# 상세 크롤링
def detail(detail_url):
    if detail_url.find("http") < 0 and  detail_url.find("https"):
        detail_url = "https:" + detail_url
        
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    title_head = detail_soup.find("div", {"class" : "box01"})
    title = title_head.find("h1").text #제목
    
    writer = ""
    
    if detail_soup.find("span", {"class" : "report"}) != None:
        writer = detail_soup.find("span", {"class" : "report"}).text #작성자
    
    content = detail_soup.find("div" , {"class" : "detail"}).text #본문
    
    all_date =detail_soup.find("span" , {"class" : "time"})
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