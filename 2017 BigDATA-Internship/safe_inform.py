#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import MySQLdb
import time
import random
import re

con = MySQLdb.connect("localhost","root","0000","test")
con.set_character_set('utf8')
cur = con.cursor()

url = 'http://www.safetykorea.kr/release/certificationsearch?selectedOption=0&textWord=&pageNo='

def pageTotal():
    html=requests.get(url+'0')
    soup=BeautifulSoup(html.text, 'lxml')
    title = soup.find('div',attrs={'class':'page'})
    b_=title.find_next('script')

    page = b_.get_text().strip()[16:21]

    print("Total Page : " + page)
    
    return int(page)

def getTable(pageNum):
    html=requests.get(url+str(pageNum))
    soup=BeautifulSoup(html.text, 'lxml')
    titles = soup.select('html table tr[style]')

    sql = "insert into safety_inform(model, product, cert, certNum) values (%s, %s, %s, %s)"
    
    for title in titles:
        model = title.select('td')[1].get_text().strip()
        model = re.sub("\n"," ", model)
        model = re.sub("'", "‘", model)
        product = title.select('td')[2].get_text().strip()
        cert = title.select('td')[3].get_text().strip()
        certNum = title.select('td')[4].get_text().strip()

        values=(model,product,cert,certNum)
        cur.execute(sql, values)
        con.commit()

def main():
    total_page = pageTotal()
    #cur.execute("delete from kats")
    #cur.execute("alter table kats auto_increment=1")
    
    for i in range(32569,total_page):
        wait_time=random.randint(3,8)
        tags = getTable(i)
        print('{0} page success'.format(i+1))
        if i%10 == 0:
            print('wait time = {0}'.format(wait_time))
            time.sleep(wait_time)
            
    print('END')
    
if __name__=='__main__':
    main()
