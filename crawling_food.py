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

url='http://tour.jecheon.go.kr/ktour/selectClturCntntsList.do?scrit1.sc1=503000&scrit1.sc2=all&scrit1.so1=X.CLTUR_CNTNTS_NO&scrit1.sa3=10&scrit1.sa3=20&scrit1.sa3=30&scrit1.sa3=40&scrit1.sa3=50&scrit1.sa3=70&scrit1.rcpp=9&key=121&scrit1.cpn='

def findUrl(number):
    html=requests.get(url+str(number))
    soup=BeautifulSoup(html.text, 'lxml')
    titles_url=soup.find_all('div', class_='photo_area')
    
    return_url = []
    
    for url_ in titles_url:
        urll=url_.find('a')
        turl='http://tour.jecheon.go.kr/{0}'.format(urll['href'])
        print(turl)
      
        #return_url.append(turl)
    
    #return return_url

def insertQuery(dUrl):
    html=requests.get(dUrl)
    soup=BeautifulSoup(html.text, 'lxml')
    title=soup.select('div[class="view_top_tit"]')
    titles=soup.select('tbody tr td')
    titles_intro=soup.select('div[class="attraction_subject"] p')
    image_url=soup.find('div',class_='attraction_img')
    i_url=image_url.find_next('img')

    try:
        go_home = soup.find('a',class_='g_btn_more')['href']
    except TypeError as e:
        go_home = ''
        
    sql = "insert into food(name, phone, address, region, time, text, image_url, home_url) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    city=title[0].get_text().strip()[1:4]
    name_=title[0].select('span')
    name=name_[0].get_text().strip()
    address=titles[0].get_text().strip()
    phone_=titles[1].select('span')
    phone=phone_[0].get_text().strip()
    menu=titles[2].get_text().strip()
    utime=titles[3].get_text().strip()
    intro = re.sub('<br/>','\n',str(titles_intro[1]))
    intro = re.sub('<p>|</p>|"','',intro)
    image = i_url['src']

    text = '대표메뉴\n' + menu +'\n메뉴안내\n' + intro
    
    if image[0:4] != 'http':
        image='http://tour.chungbuk.go.kr{0}'.format(i_url['src'])
        
    values = (name,phone,address,city,utime,text,image,go_home)
    #print(text)
    #cur.execute(sql, values)
    #con.commit()


urls=findUrl(1)
