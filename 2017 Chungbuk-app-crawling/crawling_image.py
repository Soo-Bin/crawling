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

url='http://tour.chungbuk.go.kr/home/sub.php?menukey=226&page='

def findUrl(number):
    html=requests.get(url+str(number))
    soup=BeautifulSoup(html.text, 'lxml')
    titles_url=soup.find_all('a', class_='g_over')

    return_url = []
    
    for url_ in titles_url:
        turl='http://tour.chungbuk.go.kr/home/{0}'.format(url_['href'])
        return_url.append(turl)
    
    return return_url

def insertQuery(dUrl):
    html=requests.get(dUrl)
    soup=BeautifulSoup(html.text, 'lxml')
    title=soup.select('div[class="view_top_tit"]')
    titles=soup.select('tbody tr td')
    images=soup.select('div[class="attraction_img"] img')
    
    sql = "insert into image values (%s, %s, %s)"

    name=title[0].select('span')[0].get_text().strip()
    address=titles[0].get_text().strip()
    
    for image in images:
        imagee = image['src']
        
        if imagee.find('http') == -1:
            imagee='http://tour.chungbuk.go.kr{0}'.format(image['src'])
        imagee=re.sub('http://tour.chungbuk.go.krhttp://www.chungbuknadri.net',\
              'http://www.chungbuknadri.net',imagee)
        values=(name, address, imagee)
        #print(values)
        cur.execute(sql, values)
        con.commit()
    
def main():
    #urls=findUrl(1)
    #insertQuery(urls[7])
    
    #cur.execute("delete from image")
    for j in range(1,20):
        wait_time=random.randint(3,8)
        urls=findUrl(j)
        for i in range(0,int(len(urls))):    
            uurl=urls[i]
            insertQuery(uurl)
        print('{0} page success'.format(j))
        if j%7 == 0:
            print('wait time = {0}'.format(wait_time))
            time.sleep(wait_time)

    print('END')
    con.close()

if __name__=='__main__':
    main()
