from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import csv
import re

base_url = "https://www.ytn.co.kr/" # YTN 뉴스
f = open("C:/hm_py/crawling/result/crawling_hw7.txt", "w", encoding="utf-8")
cf = open("C:/hm_py/crawling/result/rawling_hw7.csv",'w', newline='', encoding="utf-8")

wr = csv.writer(cf)
wr.writerow(['제목', '작성자', '등록일', '내용'])
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"now01 YTN_CSA_bottomnews1"}) #윗줄, 아랫줄 같이 추출 가능할까?
    items = root.find_all("ul")

    for item in items:
        data = item.find("li")
        link = data.find("a")
        link_url = link.get('href')
        
        detail(link_url) #윗줄의 앞의 칸만 열림
    
       
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    top = detail_soup.find("div", {"class":"top"})
    title = top.find("h3").text #제목
    
    writer =  "";
    # etail_soup.find("span", {"class":"author"}).text #작성자 #기자가 택스트 내에 들어가 있어서 영역을 어떻게 잡아야 할지 모르겠음
    
    content = detail_soup.find("div" , {"class" : "article"}) .text #본문 
    
    reg_date = "";
            
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
        
def main(): 
    driver.get(base_url)
    
    crawling()
    
    # 파일 닫기
    f.close()
    cf.close()

    driver.quit()
    
if __name__ == '__main__':
    main()
  