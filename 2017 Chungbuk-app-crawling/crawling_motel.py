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
    titles_intro=soup.select('div[class="attraction_subject"] li')
    image_url=soup.find('div',class_='attraction_img')
    i_url=image_url.find_next('img')

    try:
        go_home = soup.find('a',class_='g_btn_more')['href']
    except TypeError as e:
        go_home = ''
        
    sql = "insert into motel(name, phone, address, region, time, text, image_url, home_url) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    city=title[0].get_text().strip()[1:4]
    name=title[0].select('span')[0].get_text().strip()
    address=titles[0].get_text().strip()
    phone=titles[1].select('span')[0].get_text().strip()
    utime=titles[3].get_text().strip()
    text=''
    
    for i in range(1,6):
        text = text + titles_intro[i].get_text().strip() + '\n'
        
    image = i_url['src']

    if image[0:4] != 'http':
        image='http://tour.chungbuk.go.kr{0}'.format(i_url['src'])
        
    values = (name,phone,address,city,utime,text,image,go_home)
    #print(text)
    cur.execute(sql, values)
    con.commit()
    
def main():
    #urls=findUrl(1)
    #insertQuery(urls[0])

    
    cur.execute("delete from motel")
  
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
