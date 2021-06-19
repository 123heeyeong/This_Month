#뮤지컬 크롤링
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

def musical():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://ticket.interpark.com/tiki/special/TPCalendar.asp"
    soup = inputUrl(dr, url)
    elem = musicalCrawl(soup)
    printDataMusical(elem)

def musicalCrawl(soup):
    eventList = soup.select('td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a > b')
    print(eventList)
    eventDate = soup.select('td[width=100]')
    print(eventDate)
    eventHall = soup.select('td[width=120]')
    print(eventHall)
    eventTitle = "뮤지컬"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (idx, eventList[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1], eventHall[i].string)
        elem = elem + (elemNew,)
    return elem

def printDataMusical(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))

musical()
