from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101" #네이버 경제 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw1.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/rawling_hw1.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"section_body"})
    items = root.find_all("dl")
    datas = []

    for item in items:
        data = item.find("dt") 
        link = data.find("a")
        link_url = link.get('href')
        
        datas.append(detail("https://news.naver.com" + link_url))

    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(TEXT_FILE_PATH, datas, CSV_HEADER)
            
       
#상세 크롤링
def detail(detail_url):
    driver.get(detail_url)
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    title = detail_soup.find("h3", {"class" : "tts_head"}).text #제목
    writer = detail_soup.find("p", {"class" : "b_text"}).text #작성자
    content = detail_soup.find("div", {"class" : "_article_body_contents article_body_contents"}).text #본문

 
    all_date =detail_soup.find("div" , {"class" : "sponsor"})
    dates =all_date.find_all("span")
    
    if len(dates) > 1:
        reg_date = dates[1].text  # 수정일
    else:
        reg_date = dates[0].text  # 입력일

            
    data = {"title":title, "writer":writer, "content":content, "reg_date":reg_date}
    return data 
 
 
def main(): 
    driver.get(base_url)
    
    crawling()
    
    driver.quit()
    
if __name__ == '__main__':
    main()