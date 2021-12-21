from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://www.khan.co.kr/" # 경향신문 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw8.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw8.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("ul", {"class":"sub-news-wrap scroll_start02_in"})
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
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class":"headline"}).text #제목
    writer = detail_soup.find("span", {"class":"author"}).text #작성자
    content = detail_soup.find("div" , {"class" : "art_body"}).text #본문 
    
    all_date =detail_soup.find("div" , {"class" : "byline"})
    dates =all_date.find_all("em")
    
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
  