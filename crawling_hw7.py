from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import utils.file_util as file_util

base_url = "https://www.ytn.co.kr/" # YTN 뉴스
TEXT_FILE_PATH = "C:/hm_py/crawling/result/crawling_hw7.txt"
CSV_FILE_PATH = "C:/hm_py/crawling/result/rawling_hw7.csv"
CSV_HEADER = ['제목', '작성자', '등록일', '내용']
    
driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정

# 크롤링
def crawling():
    html = driver.page_source
    soup = bs(html, 'html.parser')
    root = soup.find("div", {"class":"now01 YTN_CSA_bottomnews1"}) #윗줄, 아랫줄 같이 추출 가능할까?
    items = root.find_all("ul")  # 1열만 인식하는 느낌?
    datas = []
    
    for item in items:
        data = item.find("li")
        link = data.find("a")
        link_url = link.get('href')
        
        detail(link_url) #윗줄의 앞의 칸만 열림
    
        datas.append(detail(link_url))
     
    file_util.file_writer(TEXT_FILE_PATH , datas)
    file_util.csv_writer(TEXT_FILE_PATH, datas, CSV_HEADER)
                       
# 상세 크롤링
def detail(detail_url):
    driver.get(detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')
    
    top = detail_soup.find("div", {"class":"top"})
    title = top.find("h3").text #제목
    
    writer = ""
    
    # orgin_content = detail_soup.find("div" , {"class" : "tx"})
    # str_content = str(orgin_content)
    
    # writers = str(orgin_content).split('<br/>')
    # real_writer = ""
    
    # for writer in writers:
    #     if writer.find('@kmib.co.kr') > 0:
    #         real_writer = writer 
            
    section = detail_soup.find("div" , {"class" : "article"})
    content = section.find("span").text #본문
    
    # content = relace_tag(str_content.replace('<br/>', '\n')) #본문
    
    dates =detail_soup.find_all("span", {"class" : "time"})
    
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
  