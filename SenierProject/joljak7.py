#GS25 크롤링
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# target page 접근, html source 추출 & 구문분석
def inputUrl(dr, url):
    dr.get(url)
    html_source = dr.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    return soup

def gs25():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://gs25.gsretail.com/gscvs/ko/customer-engagement/event/current-events#;"
    soup = inputUrl(dr, url)
    elem = gs25Crawl(soup)
    printDataGs25(elem)

def gs25Crawl(soup):
    page_list = soup.select('.paging .num a')
    maximum = len(page_list)

    eventList = soup.select('.ft_lt .evt_info .tit a')
    print(eventList)
    eventDate = soup.select('.ft_lt .evt_info .period')
    print(eventDate)
    eventTitle = "GS25"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (idx, eventList[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1])
        elem = elem + (elemNew,)
    return elem

def printDataGs25(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))

gs25()
