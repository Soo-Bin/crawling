#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import MySQLdb
import time
import random
import re

con = MySQLdb.connect("","tjrwnwkd21","ddugjoo21","contest")
con.set_character_set('utf8')
cur = con.cursor()

url='http://maps.googleapis.com/maps/api/geocode/xml?address='

def findLocation(name,address):
    html=requests.get(url+address)
    soup=BeautifulSoup(html.text, 'lxml')
    try:
        lat=soup.find('lat').get_text()
        lng=soup.find('lng').get_text()
    except AttributeError as e:
        lat=''
        lng=''
        
    sql="update motel set longitude=%s, latitude=%s where name=%s"
    values=(lng,lat,name)

    cur.execute(sql,values)
    con.commit()
    
def insertQuery():
    sql="select name,address from motel"
    cur.execute(sql)
    rows=cur.fetchall()
    j=0
    
    for row in rows:
        wait_time=random.randint(3,8)
        start=row[1].find('(')
        if start != -1:
            findLocation(row[0],row[1][0:int(start)])
        else:
            findLocation(row[0],row[1])
        print(row[0]+ ' '+str(start))
        if j%14 == 0:
            print('wait time = {0}'.format(wait_time))
            time.sleep(wait_time)
        j=j+1
        
def main():
    insertQuery()
    
    print('END')
    con.close()

if __name__=='__main__':
    main()
