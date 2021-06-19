#뷰티 크롤링
from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def stratSearch(key):
    if key == 1:
        eventList, eventDate, event_title = oliveyoung()
    elif key == 2:
        eventList, eventDate, event_title = lalavela()
    elif key == 3:
        eventList, eventDate, event_title = lohbs()

    print(event_title, '이벤트 목록')
    for i in range(len(eventList)):
        idx = i + 1
        elem = (idx, eventList[i].string, eventDate[i].string.split('-')[0], eventDate[i].string.split('-')[1], event_title)
        print('결과 : {}'.format(elem))


def inputUrl(url):
    res = req.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(res, "html.parser")
    return soup

def oliveyoung(): #완성
    url = 'https://www.oliveyoung.co.kr/store/main/getEventList.do'
    soup = inputUrl(url)
    eventList = soup.select("ul.event_thumb_list  p.evt_tit")
    eventDate = soup.select("ul.event_thumb_list p.evt_date")
    event_title = "올리브영"
    return eventList, eventDate, event_title

def lalavela():
    url = 'http://lalavla.gsretail.com/lalavla/ko/customer-engagement/event/current-events'
    res = req.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(res, "html.parser")
    eventList = soup.select("tr > .ft_lt .tit")
    eventDate = soup.select("tr > .ft_lt .period")
    event_title = "랄라블라"
    return eventList, eventDate, event_title

def lohbs(): # 미완성
    url = 'https://www.lotteon.com/p/display/shop/seltDpShop/12929?callType=menu'
    soup = inputUrl(url)
    eventList = soup.select(".evt_info p.tit")
    eventDate = soup.select(".evt_info p.preiod")
    event_title = "롭스"
    return eventList, eventDate, event_title

stratSearch(1)
