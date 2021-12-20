from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://www.chosun.com/" # 조선일보 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw9.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/rawling_hw9.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"flex-chain__column flex-chain__column-1 | box--bg-undefined grid__col--sm-8 grid__col--md-8 grid__col--lg-8 box--margin-right-md"})
    datas = []
    
    for item in root:
        # data = item.find("div", {"class":"story-card-component story-card__headline-container | text--overflow-ellipsis text--left"})
        link = item.find("a")
        link_url = link.get('href')
    
        datas.append(detail(base_url + link_url))
     
    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(TEXT_FILE_PATH, datas, CSV_HEADER)
    
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class":"article-header__headline | font--primary text--black"}).text # 제목
    writer = detail_soup.find("a", {"class":"article-byline__author | text--wrap-pre text--black text__link--underline"}).text #작성자
    content = detail_soup.find("section" , {"class" : "article-body"}).text # 본문

    dates =detail_soup.find_all("span", {"class" : "font--size-sm-14 font--size-md-14 text--grey-60"})
    
    if len(dates) > 1:
        reg_date = dates[1].text  # 수정일
    else:
        reg_date = dates[0].text  # 입력일

            
    data = {"title":title, "writer":writer, "content":content, "reg_date":reg_date} #데이터 약간 이상한 것 같음
    return data 

def main(): 
    driver.get(base_url)
    
    crawling()
    
    driver.quit()
    
if __name__ == '__main__':
    main()
  