from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def openFile(key):
    f = open('C:/Users/eodbs/OneDrive/test.csv','w', encoding='utf-8-sig', newline='')
    wr = csv.writer(f, delimiter=',')
    if key == 1:
        eventList, eventDate, event_title = oliveyoung()
    elif key == 2:
        eventList, eventDate, event_title = lalavela()

    print('{} 이벤트 목록', event_title)
    for i in range(len(eventList)):
        idx = i + 1
        elem = [eventList[i].string, eventDate[i].string]
        print('{}. 결과 : {}'.format(idx, elem))
        wr.writerow(elem)

    f.close()

def inputUrl(url):
    res = req.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(res, "html.parser")
    return soup

def oliveyoung(): #완성
    url = 'https://www.oliveyoung.co.kr/store/main/getEventList.do'
    soup = inputUrl(url)
    eventList = soup.select("ul.event_thumb_list .evt_tit")
    eventDate = soup.select("ul.event_thumb_list .evt_date")
    event_title = "올리브영"
    return eventList, eventDate, event_title

def lalavela(): #웹크롤링 막아놈ㅠㅠ
    url = 'http://lalavla.gsretail.com/lalavla/ko/customer-engagement/event/current-events'
    soup = inputUrl(url)
    eventList = soup.select("ft_lt .tit")
    eventDate = soup.select("ft_lt .period")
    event_title = "랄라블라"
    return eventList, eventDate, event_title

def lohbs(): # 미완성
    url = 'http://lalavla.gsretail.com/lalavla/ko/customer-engagement/event/current-events'
    soup = inputUrl(url)
    eventList = soup.select("tr > .ft_lt .tit")
    eventDate = soup.select("tr > .ft_lt .period")
    event_title = "랄라블라"
    return eventList, eventDate, event_title

openFile(1)
