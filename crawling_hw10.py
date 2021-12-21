from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util
import utils.string_util as string_util

base_url = "http://www.kmib.co.kr/news/index.asp" # 국민일보 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw10.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw10.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("dd", {"class":"rel_lst"})
    items = root.find_all("a")
    datas = []
    
    for item in items:
    
        datas.append(detail(item.get('href')))
    
    
    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(CSV_FILE_PATH, datas, CSV_HEADER)
    
    
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
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


    return [ title, real_writer, reg_date, content ]

        
def main(): 
    driver.get(base_url)
    
    crawling()

    driver.quit()
    
if __name__ == '__main__':
    main()
  