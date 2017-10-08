#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import MySQLdb
import re

con = MySQLdb.connect("localhost","root","0000","dump")
con.set_character_set('utf8')
cur = con.cursor()

url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&ie=utf8&query='

keyword = str(input('keyword : '))
start_date = str(input('start date : '))
end_date = str(input('end date : '))

date = '&nso=so%3Ar%2Cp%3Afrom' + start_date + 'to' + end_date + '%2Ca%3Aall'

def query_name(html):
    html=requests.get(html)
    soup=BeautifulSoup(html.text, 'lxml')
    title = soup.find_all('a', attrs={'class':'_sp_each_title'})
    cur.execute("delete from mews")
    #cur.execute("alter table mews auto_increment=1")
    
    for titles in title:
        print(titles.get_text())
        title2=re.sub("'", "‘", titles.get_text())
        sql="insert into mews(titles) values (%s)" % ("'" + title2 + "'")
        cur.execute(sql)
        con.commit()

def main():
    html = url+keyword+date
    query_name(html)

    print('END')
    con.close()

if __name__=='__main__':
    main()
