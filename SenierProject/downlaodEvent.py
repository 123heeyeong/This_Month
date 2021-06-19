#selenium이용해서 동적 웹크롤링
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
import sys
import io
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

#DB연결
host_name = "test.c4ip3g51hybi.ap-northeast-2.rds.amazonaws.com"
username = "admin"# MySQL 계정 아이디
password = "password" # MySQL 계정 패스워드
dbname = "diary"  # DATABASE 이름
db=pymysql.connect(host=host_name, port=3306, user=username, passwd=password, db=dbname, charset="utf8")
curs = db.cursor()
curs.execute("set names utf8")

# target page 접근, html source 추출 & 구문분석
def inputUrl(dr, url):
    dr.get(url)
    html_source = dr.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    return soup

#web webdriver실행 및 랄라블라 주소 입력
def lalavla():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://lalavla.gsretail.com/lalavla/ko/customer-engagement/event/current-events"
    soup = inputUrl(dr, url)
    elem = lalavlaCrawl(soup)
    printDataLalavla(elem)

#랄라블라 데이터 크롤링 후 데이터가공
def lalavlaCrawl(soup):
    eventList = soup.select('td.ft_lt p.tit a')
    eventDate = soup.select('td.ft_lt p.period')
    eventTitle = "랄라블라"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventDate[i].contents[1].split(' ~ ')[0],
        eventDate[i].contents[1].split(' ~ ')[1], eventTitle)
        elem = elem + (elemNew,)
    return elem

#랄라블라 데이터 출력
def printDataLalavla(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into lalavla(id,area_id, title, start_date, end_date, location) values (NULL, 1, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
        print('크롤링 데이터 전송 완료')

#web webdriver실행 및 올리브영 주소 입력
def oliveyoung():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "https://www.oliveyoung.co.kr/store/main/getEventList.do"
    soup = inputUrl(dr, url)
    elem = oliveyoungCrawl(soup)
    printDataOliveyoung(elem)

#올리브영 데이터 크롤링 후 데이터가공
def oliveyoungCrawl(soup):
    eventList = soup.select("ul.event_thumb_list  p.evt_tit")
    eventDate = soup.select("ul.event_thumb_list p.evt_date")
    eventTitle = "올리브영"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventDate[i].string.split('-')[0],
        eventDate[i].string.split('-')[1], eventTitle)
        elem = elem + (elemNew,)
    return elem

#올리브영 데이터 출력
def printDataOliveyoung(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into oliveyoung(id,area_id, title, start_date, end_date, location) values (NULL, 1, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#web webdriver실행 및 KBO 주소 입력
def kbo():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "https://sports.news.naver.com/kbaseball/schedule/index.nhn"
    soup = inputUrl(dr, url)
    elem = kboCrawl(soup)
    printDataBaseball(elem)

#KBO 데이터 크롤링 후 데이터가공
def kboCrawl(soup):
    #홀수 일 데이터 파싱
    team_lft1 = soup.select(".sch_tb span.team_lft")
    team_rgt1 = soup.select(".sch_tb span.team_rgt")
    event_date1 = soup.select(".sch_tb span.td_date > strong")
    event_hour1 = soup.select(".sch_tb span.td_hour")
    event_stadium1 = soup.select(".sch_tb span.td_stadium")
    #짝수 일 데이터 파싱
    team_lft2 = soup.select(".sch_tb2 span.team_lft")
    team_rgt2 = soup.select(".sch_tb2 span.team_rgt")
    event_date2 = soup.select(".sch_tb2 span.td_date > strong")
    event_hour2 = soup.select(".sch_tb2 span.td_hour")
    event_stadium2 = soup.select(".sch_tb2 span.td_stadium")
    eventTitle = "KBO리그"
    #중복 횟수 측정
    td_rowspan = soup.find_all(rowspan=True)
    #짝수 일 데이터 입력
    k = 0
    elem = ()
    for i in range(len(event_date2)):
        span = td_rowspan[i * 2 + 1]['rowspan']
        for j in range(0,int(span)):
            idx = k + 1
            if (event_hour2[k].string == '-'):
                del event_hour2[k]
                break
            eventDate = '21.' + event_date2[i].string + '.' + event_hour2[k].string
            eventList = team_lft2[k].string + 'vs' + team_rgt2[k].string
            elemNew = (eventDate, eventList,
            event_stadium2[2 * idx - 1].string, eventTitle)
            elem = elem + (elemNew,)
            k = k + 1
    idx2 = idx + 1
    #홀수 일 데이터 입력
    i=j=k=0
    for i in range(len(event_date1)):
        span = td_rowspan[i*2]['rowspan']
        for j in range(0,int(span)):
            idx = k + 1
            if (event_hour1[k].string == '-'):
                del event_hour1[k]
                break
            eventDate = '21.' + event_date1[i].string + '.' + event_hour1[k].string
            eventList = team_lft1[k].string + 'vs' + team_rgt1[k].string
            elemNew = (eventDate, eventList,
            event_stadium1[2 * idx - 1].string, eventTitle)
            elem = elem + (elemNew,)
            k = k + 1
            idx2 = idx2 + 1
    return elem

#야구 데이터 출력
def printDataBaseball(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into baseball_event(id,area_id, date, game, stadium, broadcast) values (NULL, 2, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#뮤지컬
def musical():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://ticket.interpark.com/tiki/special/TPCalendar.asp"
    soup = inputUrl(dr, url)
    elem = musicalCrawl(soup)
    printDataMusical(elem)

def musicalCrawl(soup):
    eventList = soup.select('td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a > b')
    eventDate = soup.select('td[width=100]')
    eventHall = soup.select('td[width=120]')
    eventTitle = "뮤지컬"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventHall[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1])
        elem = elem + (elemNew,)
    return elem

#뮤지컬 데이터 출력
def printDataMusical(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into Musical(id, area_id, title, location, start_date, end_date) values (NULL, 4, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#연극
def act():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://ticket.interpark.com/tiki/special/TPCalendar.asp?ImgYn=Y&Ca=&KindOfGoods=01009&KindOfFlag=P&PlayDate=20210525"
    soup = inputUrl(dr, url)
    elem = actCrawl(soup)
    printDataAct(elem)

def actCrawl(soup):
    eventList = soup.select('td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a > b')
    eventDate = soup.select('td[width=100]')
    eventHall = soup.select('td[width=120]')
    eventTitle = "연극"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventHall[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1])
        elem = elem + (elemNew,)
    return elem

#연극 데이터 출력
def printDataAct(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into act(id, area_id, title, location, start_date, end_date) values (NULL, 4, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#클래식
def classic():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://ticket.interpark.com/tiki/special/TPCalendar.asp?ImgYn=Y&Ca=&KindOfGoods=01004&KindOfFlag=P&PlayDate=20210525"
    soup = inputUrl(dr, url)
    elem = classicCrawl(soup)
    printDataClassic(elem)

def classicCrawl(soup):
    eventList = soup.select('td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a > b')
    eventDate = soup.select('td[width=100]')
    eventHall = soup.select('td[width=120]')
    eventTitle = "클래식"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventHall[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1])
        elem = elem + (elemNew,)
    return elem

#클래식 데이터 출력
def printDataClassic(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into classic(id, area_id, title, location, start_date, end_date) values (NULL, 4, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#전시
def exhibition():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "http://ticket.interpark.com/tiki/special/TPCalendar.asp?ImgYn=Y&Ca=&KindOfGoods=01008&KindOfFlag=P&PlayDate=20210525"
    soup = inputUrl(dr, url)
    elem = exhibitionCrawl(soup)
    printDataExhibition(elem)

def exhibitionCrawl(soup):
    eventList = soup.select('td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a > b')
    eventDate = soup.select('td[width=100]')
    eventHall = soup.select('td[width=120]')
    eventTitle = "전시"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (eventList[i].string, eventHall[i].string, eventDate[i].text.split('~')[0], eventDate[i].text.split('~')[1])
        elem = elem + (elemNew,)
    return elem

#전시 데이터 출력
def printDataExhibition(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into exhibition(id, area_id, title, location, start_date, end_date) values (NULL, 4, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#일상 - gs25
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

#일상 데이터 출력
def printDataGs25(elem):
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert ignore into exhibition(id, title, start_date, end_date) values (NULL, 4, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

lalavla()
oliveyoung()
kbo()
musical()
act()
classic()
exhibition()
gs25()

db.close()  #DB 연결 종료
