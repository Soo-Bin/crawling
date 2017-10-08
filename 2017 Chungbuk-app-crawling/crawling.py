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

url='http://tour.chungbuk.go.kr/home/sub.php?menukey=222&page='

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
    titles=soup.select('tbody tr td')
    title=soup.select('div[class="view_top_tit"]')
    titles_intro=soup.select('div[class="attraction_subject"] p')
    image_url=soup.find('div',class_='attraction_img')
    i_url=image_url.find_next('img')

    try:
        go_home = soup.find('a',class_='g_btn_more')['href']
    except TypeError as e:
        go_home = ''
        
    sql = "insert into tour(name, phone, address, region, text, time, image_url, home_url) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    city = title[0].get_text().strip()[1:4]
    name_ = title[0].select('span')
    name = name_[0].get_text().strip()
    address = titles[0].get_text().strip()
    phone_= titles[1].select('span')
    phone = phone_[0].get_text().strip()
    utime = titles[2].get_text().strip()
    intro = titles_intro[0].get_text().strip()
    image = i_url['src']

    if image[0:4] != 'http':
        image='http://tour.chungbuk.go.kr{0}'.format(i_url['src'])
    
    values = (name,phone,address,city,intro,utime,image,go_home)
    #print(values)
    cur.execute(sql, values)
    con.commit()
    
def main():
    #urls=findUrl(1)
    #insertQuery(urls[2])
    
    cur.execute("delete from tour")
    nid=1;
    for j in range(1,91):
        wait_time=random.randint(3,8)
        urls=findUrl(j)
        for i in range(0,int(len(urls))):    
            uurl=urls[i]
            if nid != 257:
                insertQuery(uurl)
            nid=nid+1
        print('{0} page success \t nid = {1}'.format(j,nid-1))
        if j%7 == 0:
            print('wait time = {0}'.format(wait_time))
            time.sleep(wait_time)
 
    print('END')
    con.close()

if __name__=='__main__':
    main()
