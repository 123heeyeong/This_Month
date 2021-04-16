from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

url = "https://www.oliveyoung.co.kr/store/main/getEventList.do"
res = req.urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(res, "html.parser")

f = open('c:/section2/write.csv','w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)

eventList = soup.select("ul.event_thumb_list .evt_tit")
eventDetail = soup.select("ul.event_thumb_list .evt_desc")
eventDate = soup.select("ul.event_thumb_list .evt_date")

print('올리브영 이벤트 목록')
for i in range(len(eventList)):
    idx = i + 1
    elem = (eventList[i].string, eventDetail[i].string, eventDate[i].string)
    print('{}. 결과 : {}'.format(idx, elem))
    wr.writerow(elem)

f.close()
