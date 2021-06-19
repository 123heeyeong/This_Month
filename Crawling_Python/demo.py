#demo 동작 설명을 위해 wait 사용
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
    wait = input("PRESS ENTER TO CONTINUE.")
    elem = lalavlaCrawl(soup)
    printDataBeauty(elem)

#랄라블라 데이터 크롤링 후 데이터가공
def lalavlaCrawl(soup):
    eventList = soup.select('td.ft_lt p.tit a')
    eventDate = soup.select('td.ft_lt p.period')
    eventTitle = "랄라블라"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (idx + 100, eventList[i].string, eventDate[i].contents[1].split(' ~ ')[0],
        eventDate[i].contents[1].split(' ~ ')[1], eventTitle)
        elem = elem + (elemNew,)
    return elem

#web webdriver실행 및 올리브영 주소 입력
def oliveyoung():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "https://www.oliveyoung.co.kr/store/main/getEventList.do"
    soup = inputUrl(dr, url)
    elem = oliveyoungCrawl(soup)
    printDataBeauty(elem)

#올리브영 데이터 크롤링 후 데이터가공
def oliveyoungCrawl(soup):
    eventList = soup.select("ul.event_thumb_list  p.evt_tit")
    eventDate = soup.select("ul.event_thumb_list p.evt_date")
    eventTitle = "올리브영"
    elem = ()
    for i in range(len(eventList)):
        idx = i + 1
        elemNew = (idx+200, eventList[i].string, eventDate[i].string.split('-')[0],
        eventDate[i].string.split('-')[1], eventTitle)
        elem = elem + (elemNew,)
    return elem

#web webdriver실행 및 KBO 주소 입력
def kbo():
    dr = webdriver.Chrome('C:/chromedriver.exe')
    url = "https://sports.news.naver.com/kbaseball/schedule/index.nhn"
    soup = inputUrl(dr, url)
    elem = kboCrawl(soup)
    printDataSport(elem)

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
            elemNew = (idx+1000, eventDate, eventList,
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
            elemNew = (idx2+1000, eventDate, eventList,
            event_stadium1[2 * idx - 1].string, eventTitle)
            elem = elem + (elemNew,)
            k = k + 1
            idx2 = idx2 + 1
    return elem

#데이터 출력
def printDataBeauty(elem):
    print(elem[0][4], '이벤트 목록')
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert into area_cal(id,area_id, title, start_date, end_date, location) values (%s, 1, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

#데이터 출력
def printDataSport(elem):
    print(elem[0][4], '경기 일정')
    for i in range(len(elem)):
        print('결과 : {}'.format(elem[i]))
        query = "insert into baseball_event(id,area_id, date, game, stadium, broadcast) values (%s, 2, %s, %s, %s, %s)"
        curs.execute(query, elem[i])
        db.commit()
    print('크롤링 데이터 전송 완료')

lalavla()
oliveyoung()
kbo()
db.close()
