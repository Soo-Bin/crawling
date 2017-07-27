#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import MySQLdb
import random
import time
import re

con = MySQLdb.connect("localhost","root","0000","test")
con.set_character_set('utf8')
cur = con.cursor()

url = 'http://www.safetykorea.kr/release/certDetail?certNum='

def insertDetail(certNum):
    html=requests.get(url+str(certNum))
    soup=BeautifulSoup(html.text, 'lxml')
    tables = soup.select('html table[class]')

    certInfo = tables[0].select('td')
    prodInfo = tables[1].select('td')
    makeInfo = tables[2].select('td')
    
    certification = certInfo[0].get_text().strip()
    certNum = certInfo[1].get_text().strip()
    certDate = certInfo[3].get_text().strip()
    classify = certInfo[4].get_text().strip()
    reason = certInfo[5].get_text().strip()

    brand = prodInfo[2].get_text().strip()
    prodCode = prodInfo[3].get_text().strip()
    income = prodInfo[4].get_text().strip()
    derivationMod = prodInfo[5].get_text().strip()

    manufacturer = makeInfo[0].get_text().strip()
    manufCountry = makeInfo[1].get_text().strip()
    importCompany = makeInfo[2].get_text().strip()
    
    values=(certification,certNum,certDate,classify,reason,brand, prodCode, income, derivationMod,manufacturer, manufCountry, importCompany)
    
    print(values)
    
    sql = "insert into safety_inform_detail values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(tables)
    cur.execute(sql,values)
    con.commit()
    
def insertData():

    #cur.execute("delete from safety_inform_detail")
    #con.commit()
    
    sql = "select certNum from safety_inform where id between 40942 and 237080"
    #between 31609 and 237080
    i=1
    
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        wait_time=random.randint(3,8)
        insertDetail(row[0])
        print('\n\n')
        if i%10 == 0:
            print('wait time = {0}'.format(wait_time))
            time.sleep(wait_time)
        i=i+1

def main():
    
    insertData()
    print('END')
 
if __name__=='__main__':
    main()
