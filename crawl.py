



''' to do : reqeusts exception handling
                page parsing -> done
                BeautifulSoup exception handling
                modularizing -> done???
                file deduplication
                machine learning
                etc...
'''

from twice_crawler import *

if __name__ == "__main__":

    count_image = 0

    crawler = Crawler(count_image)
    crawler.crawl()
