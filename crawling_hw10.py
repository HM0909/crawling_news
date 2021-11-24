from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import csv
import re

base_url = "http://www.kmib.co.kr/news/index.asp" # 국민일보 뉴스
f = open("C:/hm_py/crawling/result/crawling_hw10.txt", "w", encoding="utf-8")
cf = open("C:/hm_py/crawling/result/rawling_hw10.csv",'w', newline='')

wr = csv.writer(cf)
wr.writerow(['제목', '작성자', '등록일', '내용'])
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("dd", {"class":"rel_lst"})
    items = root.find_all("a")
    
    for item in items:
        detail(item.get('href'))
    
    
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    head = detail_soup.find("div", {"class":"nwsti"})
    
    title = head.find("h3").text    # 제목
    
    orgin_content = detail_soup.find("div" , {"class" : "tx"})
    str_content = str(orgin_content)
    content = relace_tag(str_content.replace('<br/>', '\n'))   # 본문
 
    dates = detail_soup.find_all("span" , {"class" : "t11"})
    reg_date = "";

    if len(dates) > 1:
        reg_date = dates[1].text  # 수정일
    else:
        reg_date = dates[0].text  # 입력일

    writers = str(orgin_content).split('<br/>')
    real_writer = ""
    
    for writer in writers:
        if writer.find('@kmib.co.kr') > 0:
            real_writer = writer 
            
    file_writer(title, real_writer, reg_date, content)


# 텍스트 파일 생성
def file_writer(title, writer, reg_date, content):
    f.write(title + '\n') 
    f.write(writer + '\n')
    f.write(reg_date + '\n')
    f.write(content + '\n')
    f.write('\n')
    
    
# csv 파일 생성
def csv_writer(title, writer, reg_date, content):
    wr.writerow([title, writer, reg_date, content])
    
# 태그 제거
def relace_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext  = re.sub(cleanr, '', content)     
    
    return cleantext    
        
def main(): 
    driver.get(base_url)
    
    crawling()
    
    # 파일 닫기
    f.close()
    cf.close()

    driver.quit()
    
if __name__ == '__main__':
    main()
  