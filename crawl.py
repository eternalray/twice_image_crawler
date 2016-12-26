import re
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    ''' to do : reqeusts exception handling
                page parsing
    '''
    response = requests.get("http://gall.dcinside.com/board/view/?id=twice&no=2555429&page=2&exception_mode=recommend")

    ''' to do : BeautifulSoup exception handling '''
    soup = BeautifulSoup(response.text, 'lxml')

    image_tag = soup.find_all(attrs={ "app_paragraph" : re.compile("^Dc_App_Img_[0-9]+$"), "app_editorno" : re.compile("^[0-9]+$") }) # find the first image

    for i in range(len(image_tag)):
        image_src = image_tag[i].find('img')

        '''to do : exception handling '''
        image_response = requests.get(image_src.attrs['src'], stream=True)

        ''' file name should be determined '''
        with open('twice' + str(i) + '.jpg', 'wb') as fd:
            for chunk in image_response.iter_content(chunk_size=128):
                fd.write(chunk)
