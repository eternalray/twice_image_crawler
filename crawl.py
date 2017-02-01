



'''
        to do : reqeusts exception handling
                page parsing -> done
                BeautifulSoup exception handling
                modularizing -> done
                file deduplication
                machine learning
                implement atomicity of crawling binary -> done
                status file encryption
                making page structure
                etc...
'''

from twice_crawler import *

if __name__ == "__main__":
    try:
        if len(sys.argv) is not 2:
            print("Usage : <crawl.py> <the number of pages to crawl>")
            exit(1)
        fd = open("crawl_status.txt","r")
        fd.seek(14)
        count_image = int(fd.readline()) # get image count from crawl_status.txt
        fd.seek(31)
        prev_start_point = int(fd.readline()) # get previous crawl start point from crawl_status.txt
        fd.seek(51)
        prev_end_point = int(fd.readline()) # get previous crawl end point from crawl_status.txt
    except FileNotFoundError:
        count_image = 0 # if it is the first time doing crawling, set count_image to 0
        prev_start_point = 0
        prev_end_point = 0
    except:
        print("Exception occured. Terminating")
        raise

    crawler = Crawler(count_image,prev_start_point,prev_end_point)
    crawler.crawl()
