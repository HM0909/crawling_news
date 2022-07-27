import re

# 태그 제거
def relace_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext  = re.sub(cleanr, '', content)     
    
    return cleantext    