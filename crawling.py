import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import utils.file_util as file_utils
import logger as logger
from crawl_manager import *
from db_manager import DatabaseManager


PROJECT_NAME = "crawl"
RESULT_TEXT_FILE_NAME = "C:/hm_py/crawling_news/result/result_{}.txt"
RESULT_CSV_FILE_NAME = "C:/hm_py/crawling_news/result/result_{}.csv"
HEADER = ['제목', '작성자', '등록일', '내용']
ARGV_COUNT = 2
DATABASE_ID = "local"
    

# Create logger
logger = logger.create_logger(PROJECT_NAME)

def create_crawl_manager(journal_id):
    # get module from module name
    mod_name = "crawl.{}_crawl".format(journal_id)    
    mod = __import__('%s' %(mod_name), fromlist=[mod_name])
    
    # get class in module
    klass = getattr(mod, "{}CrawlManager".format(journal_id.capitalize()))
    
    return klass(driver)


# 크롤링
def crawling(manager, journal_id):
    urls = []
    results = []

    urls = manager.list()
    
    for url in urls:
        results.append(manager.detail(url))

    # file_utils.file_writer(RESULT_TEXT_FILE_NAME.format(journal_id), results)   
    # file_utils.csv_writer(RESULT_CSV_FILE_NAME.format(journal_id), results, HEADER)
    
    datas = []
    
    for result in results:
        result.append(journal_id)
        datas.append(result)
        
    db = DatabaseManager(DATABASE_ID)
    db.connection()
    
    query = '''
            INSERT INTO news (TITLE, LINK_URL, WRITER, PUBLISH_DATE, CONTENT, JOURNAL_ID, REG_DATE)
    		VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                now()
            )                    
        '''        

    result = db.execute_query(query, datas)
    
    
def main(args): 
    logger.info("Start crawling...")

    journal_id = args[1]

    if journal_id != None:
        manager = create_crawl_manager(journal_id)

        crawling(manager, journal_id)
        
        driver.quit()
    
    logger.info("Finished.")   
    sys.exit(1)

    
# 실행 옵션 설명
def run_info():
    print("Usage: crawling.py [OPTIONS]")
    print("")
    print("Options:")
    print("  --journal_id String     [required]")


if __name__ == '__main__':
    for i in range(len(sys.argv)):
        if i > 0:
            logger.info('arg value = %s', sys.argv[i])

    if len(sys.argv) >= ARGV_COUNT:    
        driver = webdriver.Chrome(ChromeDriverManager().install())

        main(sys.argv)
    else:
        logger.error("Requires at least %s argument, but only %s were passed.", ARGV_COUNT-1, len(sys.argv)-1)
        run_info()  