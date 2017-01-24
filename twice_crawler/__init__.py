import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque

class Crawler:

    ''' for numbering files '''
    def __init__(self,count_image):
        self.count_image = count_image

    def _isImage(self,string):
        image_pattern = "[0-9]+p|[0-9]+pic|과질|고화질|!프리뷰|!플뷰|gif|움짤|퇴근길|출근길"
        image_regex = re.compile(image_pattern)
        match = re.search(image_regex, string)
        return match

    def _crawl(sel,count,url_tag):
        for i in range(len(url_tag)):
            print("crawling " + url_tag[i].string)
            article_url = "http://gall.dcinside.com/" + url_tag[i].attrs['href']
            response = requests.get(article_url)
            soup = BeautifulSoup(response.text, 'lxml')
            tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"),"app_editorno" : re.compile("^[0-9]+$") })
            save_path = ""

            for j in range(len(tag)):
                src = tag[j].find('img')
                image_response = requests.get(src.attrs['src'],stream=True)
                save_path = "twice_img/twice" + str(count + 1)
                with open(save_path, "wb") as fd:
                    for chunk in image_response.iter_content(chunk_size=1024*1024):
                        fd.write(chunk)
                count += 1
        return count
    def crawl(self):
        start_article_number = None
        end_article_number = None
        num_of_page = sys.argv[1] # get command line argument for the number of pages to crawl, future work : find better way to do this?
        for i in range(1,int(num_of_page) + 1):
            ''' parsing page by page '''

            page_url = "http://gall.dcinside.com/board/lists/?id=twice&page=" + str(i) + "&exception_mode=recommend"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text,'lxml')

            image_url_tag = soup.find_all(attrs={ "class" : "icon_pic_b" },string=self._isImage)

            ''' if image_url_tag is None or empty, continue the loop '''

            if not image_url_tag:
                continue

            ''' assign crawling start point '''

            if start_article_number is None:
                start_article_number = image_url_tag[0].parent.find_previous_sibling("td").string

            self.count_image = self._crawl(self.count_image,image_url_tag)

        ''' assign crawling end point and log crawl status'''

        end_article_number = image_url_tag[len(image_url_tag)-1].parent.find_previous_sibling("td").string
        with open("crawl_status.txt","w") as fd:
            fd.write("count_image = " + str(self.count_image)) # log image count
