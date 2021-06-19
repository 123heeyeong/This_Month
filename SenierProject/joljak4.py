# 크롤링한 자료들을 DB로 전송
from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io
import pymysql
host_name = "test.c4ip3g51hybi.ap-northeast-2.rds.amazonaws.com"
username = "admin"# MySQL 계정 아이디
password = "password" # MySQL 계정 패스워드
dbname = "diary"  # DATABASE 이름

db=pymysql.connect(
host=host_name,
port=3306,
user=username,
passwd=password,
db=dbname,
charset="utf8"
)
curs = db.cursor()
curs.execute("set names utf8")

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
        elem = (str(idx), eventList[i].string, eventDate[i].string.split('- ')[0], eventDate[i].string.split('-')[1], event_title)
        print('결과 : {}'.format(elem))
        query = "insert into area_cal(area_id, title, start_date, end_date, location) values (%s, %s, %s, %s, %s)"
        curs.execute(query, elem)
        db.commit()
    db.close()
    print('크롤링 데이터 전송 완료')

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

stratSearch(1)
