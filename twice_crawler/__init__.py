
import re
import requests
from bs4 import BeautifulSoup
from collections import deque

class Crawler:

    ''' for numbering files '''
    def __init__(self,count_image,count_gif):
        self.count_image = count_image
        self.count_gif = count_gif


    def crawl(self):

        def _is_image(string):
            image_pattern = "[0-9]+p|[0-9]+pic|과질|고화질"
            image_regex = re.compile(image_pattern)
            match = re.search(image_regex, string)
            if match and not _is_gif(string):
                return True
            else:
                return False

        def _is_gif(string):
            gif_pattern = "gif|움짤"
            gif_regex = re.compile(gif_pattern)
            match = re.search(gif_regex ,string)
            if match:
                return True
            else:
                return False

        def _crawl(count, url_tag, flag):

            for i in range(len(url_tag)):
                print("crawling " + url_tag[i].string)
                article_url = "http://gall.dcinside.com/" + url_tag[i].attrs['href']
                response = requests.get(article_url)

                soup = BeautifulSoup(response.text, 'lxml')
                tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"), "app_editorno" : re.compile("^[0-9]+$") })
                save_path = ""
                save_extension = ""

                for j in range(len(tag)):
                    src = tag[j].find('img')
                    image_response = requests.get(src.attrs['src'], stream=True)

                    if flag == "image":
                        save_path = "twice_img/twice" + str(count + 1)
                        save_extension = ".jpg"

                    elif flag == "gif":
                        save_path = "twice_gif/twice" + str(count + 1)
                        save_extension = ".gif"

                    with open(save_path + save_extension, "wb") as fd:
                        for chunk in image_response.iter_content(chunk_size=1024*1024):
                            fd.write(chunk)
                    count += 1


        for i in range(1,1000):
            page_url = "http://gall.dcinside.com/board/lists/?id=twice&page=" + str(i) + "&exception_mode=recommend"
            response = requests.get(page_url)

            soup = BeautifulSoup(response.text, 'lxml')

            ''' check whether the given url is image or gif by looking title
                future work : tell whether it is image or gif by checking magic number of binary
            '''

            image_url_tag = soup.find_all(attrs={ "class" : "icon_pic_b" }, string=_is_image)
            gif_url_tag = soup.find_all(attrs={ "class" : "icon_pic_b" }, string=_is_gif)      # these two lines are ultimately going to be merged

            _crawl(self.count_image, image_url_tag, "image")
            _crawl(self.count_gif, gif_url_tag, "gif")
