from bs4 import BeautifulSoup
import urllib.request as req
import sys
import io
import csv
import pymysql
host_name = "test.c4ip3g51hybi.ap-northeast-2.rds.amazonaws.com"
username = "admin" # MySQL 계정 아이디
password = "password" # MySQL 계정 패스워드
dbname = "sys"  # DATABASE 이름

db=pymysql.connect(
host=host_name,
port=3306,
user=username,
passwd=password,
db=dbname,
charset="utf8"
)
cursor = db.cursor()
cursor.execute("set names utf8")

def example():
    query = "insert into area(id, area) values (1, "학교")"
    cursor.execute(query)
    db.commit()

print("{}", example())
