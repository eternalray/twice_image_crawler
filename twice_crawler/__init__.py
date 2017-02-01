import sys
import re
import requests
import datetime
import os
from bs4 import BeautifulSoup

class Crawler:

    ''' for numbering files '''
    def __init__(self,count_image,prev_start_point,prev_end_point):
        self.count_image = count_image
        self.prev_start_point = prev_start_point
        self.prev_end_point = prev_end_point
        self._last_article_number = None

    def _isImage(self,string):
        image_pattern = "사진|[0-9]+[Pp]|과질|고화질|[Gg][Ii][Ff]|움짤|[출퇴]근길|[Bb][Yy]"
        exclude_pattern = "프리뷰|플뷰"
        image_regex = re.compile(image_pattern)
        exclude_regex = re.compile(exclude_pattern)
        match = re.search(image_regex,string)
        match_exclude = re.search(exclude_regex,string)
        if match_exclude is not None:
            return False
        elif match is not None:
            return True
        else:
            return False


    def _logStatus(self,start_point,end_point):
        with open("crawl_status.txt","w") as fd:
            fd.write("count_image = " + str(self.count_image) + "\n") # log image count
            fd.write("start point = " + str(start_point) + "\n") # log starting point with article number
            fd.write("end point = " + str(end_point)+ "\n") # log end point with article number`
            fd.write("crawling done in " + str(datetime.datetime.now()) + "\n") # timestamp

    def _crawl(self,url_tag):
        for i in range(len(url_tag)):
            print("crawling " + url_tag[i].string)
            if i is len(url_tag)-1:
                self._last_article_number = self._getArticleNumber(url_tag,i)
            article_url = "http://gall.dcinside.com/" + url_tag[i].attrs['href']
            response = requests.get(article_url)
            soup = BeautifulSoup(response.text, 'lxml')

            tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"),"app_editorno" : re.compile("^[0-9]+$") })

            ''' I dont know why this happens but rarely, without standard app_paragraph and app_editorno, only class name "txc-image" comes with img tag '''

            if not tag:
                tag = soup.find_all(attrs={ "class" : "txc-image" })
                for j in range(len(tag)):
                    tag[j] = tag[j].parent # had to do this because the DOM tree is totally different from normal one

            for j in range(len(tag)):
                src = tag[j].find('img')
                image_response = requests.get(src.attrs['src'],stream=True)
                save_path = "twice_img/twice" + str(self.count_image+1)
                with open(save_path, "wb") as fd:
                    try:
                        for chunk in image_response.iter_content(chunk_size=1024*1024):
                            fd.write(chunk)
                    except KeyboardInterrupt:
                        print("stop crawling twice" + str(self.count_image+1))
                        print("deleting twice" + str(self.count_image+1))
                        os.remove(save_path)
                        print("terminating...")
                        if i is not 0:
                            self._last_article_number = self._getArticleNumber(url_tag,i-1)
                        raise KeyboardInterrupt(str(self._last_article_number))
                self.count_image += 1

    def _getArticleNumber(self,url_tag,index):
        return int(url_tag[index].parent.find_previous_sibling("td").string)

    def crawl(self):
        ''' function for getting article number '''

        start_article_number = None
        end_article_number = None
        num_of_page = int(sys.argv[1]) # get command line argument for the number of pages to crawl, future work : find better way to do this?
        for i in range(1,num_of_page+1):
            ''' parsing page by page '''

            page_url = "http://gall.dcinside.com/board/lists/?id=twice&page=" + str(i) + "&exception_mode=recommend"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text,'lxml')

            image_url_tag = soup.find_all(attrs={ "class" : re.compile("icon_pic_b|sec_icon") },string=self._isImage)

            ''' if image_url_tag is None or empty, continue to crawl next page '''

            if not image_url_tag:
                continue

            ''' check if the prev_start_point or prev_end_point exists in this page, and then skip the already crawled parts '''

            page_start_number = self._getArticleNumber(image_url_tag,0)
            page_end_number = self._getArticleNumber(image_url_tag,len(image_url_tag)-1)

            if (self.prev_start_point <= page_start_number and self.prev_start_point >= page_end_number) or (self.prev_end_point <= page_start_number and self.prev_end_point >= page_end_number):
                j = 0
                while j < len(image_url_tag):
                    current_article_number = self._getArticleNumber(image_url_tag,j)
                    if current_article_number < self.prev_end_point:
                        break
                    elif current_article_number >= self.prev_end_point and current_article_number <= self.prev_start_point:
                        del image_url_tag[j]
                        j -= 1
                    elif current_article_number > self.prev_start_point:
                        j += 1
                        continue
                    j += 1

            ''' assign crawling start point '''

            if start_article_number is None:
                start_article_number = self._getArticleNumber(image_url_tag,0)
            try:
                self._crawl(image_url_tag)
            except KeyboardInterrupt as e:
                if self.count_image is 0:
                    exit(1)
                elif self.count_image > 0:
                    end_article_number = int(e.args[0])
                    self._logStatus(start_article_number,end_article_number)
                    exit(1)
                else:
                    print("internal error occured\nterminating...")

        ''' assign crawling end point and log crawl status'''

        end_article_number = self._getArticleNumber(image_url_tag,len(image_url_tag)-1)
        self._logStatus(start_article_number,end_article_number)
        exit(1)
