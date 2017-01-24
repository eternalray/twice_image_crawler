



''' to do : reqeusts exception handling
                page parsing -> done
                BeautifulSoup exception handling
                modularizing -> done???
                file deduplication
                machine learning
                implement atomicity of crawling binary
                etc...
'''

from twice_crawler import *

if __name__ == "__main__":
    try:
        fd = open("crawl_status.txt","r")
        fd.seek(14)
        count_image = int(fd.read()) # get image count from crawl_status.txt

    except FileNotFoundError:
        count_image = 0 # if it is the first time doing crawling, set count_image to 0

    crawler = Crawler(count_image)
    crawler.crawl()
