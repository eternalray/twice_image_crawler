import re
import requests
from bs4 import BeautifulSoup
from collections import deque


def is_image(string):
    image_pattern = "[0-9]+p|[0-9]+pic|과질|고화질"
    image_regex = re.compile(image_pattern)
    match = re.search(image_regex, string)
    if match and not is_gif(string):
        return True
    else:
        return False

def is_gif(string):
    gif_pattern = "gif|움짤"
    gif_regex = re.compile(gif_pattern)
    match = re.search(gif_regex ,string)
    if match:
        return True
    else:
        return False

if __name__ == "__main__":

    ''' to do : reqeusts exception handling
                page parsing -> done
                BeautifulSoup exception handling
                modularizing
    '''


    queue = deque()
    count_image = 0
    count_gif = 0
    for i in range(1,1000):
        page_url = "http://gall.dcinside.com/board/lists/?id=twice&page=" + str(i) + "&exception_mode=recommend"
        response = requests.get(page_url)

        soup = BeautifulSoup(response.text, 'lxml')

        ''' check whether the given url is image or gif by looking title
            future work : tell whether it is image or gif by checking magic number of binary
        '''

        image_url_tag = soup.find_all(attrs={ "class" : "icon_pic_b" }, string = is_image)
        gif_url_tag = soup.find_all(attrs={ "class" : "icon_pic_b" }, string = is_gif)

        for j in range(len(image_url_tag)):
            print("crawling image from " + image_url_tag[j].string)
            image_article_url = "http://gall.dcinside.com/" + image_url_tag[j].attrs['href']
            response = requests.get(image_article_url)

            soup = BeautifulSoup(response.text, 'lxml')
            image_tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"), "app_editorno" : re.compile("^[0-9]+$") })

            for a in range(len(image_tag)):

                image_src = image_tag[a].find('img')
                image_response = requests.get(image_src.attrs['src'], stream=True)

                ''' to do : file name should be determined
                            check magic number and decide the extension of file
                '''
                with open('twice_img/twice' + str(count_image + 1) + '.jpg', 'wb') as fd:
                    for chunk in image_response.iter_content(chunk_size=1024*1024):
                        fd.write(chunk)
                count_image += 1

        for k in range(len(gif_url_tag)):
            print("crawling gif from " + gif_url_tag[k].string)
            gif_article_url = "http://gall.dcinside.com/" + gif_url_tag[k].attrs['href']
            response = requests.get(gif_article_url)

            soup = BeautifulSoup(response.text, 'lxml')
            gif_tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"), "app_editorno" : re.compile("^[0-9]+$") })

            for b in range(len(gif_tag)):

                gif_src = gif_tag[b].find('img')
                gif_response = requests.get(gif_src.attrs['src'], stream=True)

                ''' to do : file name should be determined
                            check magic number and decide the extension of file
                '''
                with open('twice_gif/twice' + str(count_gif + 1) + '.gif', 'wb') as fd:
                    for chunk in gif_response.iter_content(chunk_size=1024*1024):
                        fd.write(chunk)
                count_gif += 1
