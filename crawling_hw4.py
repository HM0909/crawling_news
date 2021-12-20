from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import csv
import re

base_url = "https://www.hankyung.com/" #한국경제 뉴스

f = open("C:/hm_py/crawling/result/crawling_hw4.txt", "w", encoding="utf-8")
cf = open("C:/hm_py/crawling/result/rawling_hw4.csv",'w', newline='', encoding="utf-8")

wr = csv.writer(cf)
wr.writerow(['제목', '작성자', '등록일', '내용'])
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"main-top-major"})
    items = root.find_all("li")

    for item in items:
        link = item.find("a")
        link_url = link.get('href')
        
        detail(link_url)
    
       
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    title = get_writer(detail_soup.find("h1", {"class" : "title"}).text) #제목
    writer = get_writer(detail_soup.find("div", {"class" : "author"}).text) #작성자 #공백 없이 추출하고 싶음
    content = detail_soup.find("div" , {"id" : "articletxt"}).text #본문
    
    
    all_date =detail_soup.find("div" , {"class" : "date-info"})
    dates =all_date.find_all("span")
    
    if len(dates) > 1:
        reg_date = dates[1].text  # 수정일
    else:
        reg_date = dates[0].text  # 입력일

            
    file_writer(title, writer, reg_date, content)
    csv_writer(title, writer, reg_date, content)


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
        
        
# 텍스트 리플레스        
def get_writer(writer):
    writer = writer.replace('\n', '')
    writer = writer.replace(" ", "")
    writer = writer.replace("·", " ")
    
    return writer
    
    
def main(): 
    driver.get(base_url)
    
    crawling()
    
    # 파일 닫기
    f.close()
    cf.close()

    driver.quit()
    
if __name__ == '__main__':
    main()