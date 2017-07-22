import sqlite3
import xlrd
import xlsxwriter
import math
import matplotlib.pyplot as plt

con = sqlite3.connect("testDB")
cur = con.cursor()

while True:
    cur.execute("delete from jejutourist")
    choice = int(input("년도 선택(2010~2015, 종료시 0) : "))
    if choice == 2010:
        wb = xlrd.open_workbook('C:/python34/database/2010년.xls')
        break
    elif choice == 2011:
        wb = xlrd.open_workbook('C:/python34/database/2011년.xls')
        break
    elif choice == 2010:
        wb = xlrd.open_workbook('C:/python34/database/2011년.xls')
        break
    elif choice == 2012:
        wb = xlrd.open_workbook('C:/python34/database/2012년.xls')
        break
    elif choice == 2013:
        wb = xlrd.open_workbook('C:/python34/database/2013년.xls')
        break
    elif choice == 2014:
        wb = xlrd.open_workbook('C:/python34/database/2014년.xls')
        break
    elif choice == 2015:
        wb = xlrd.open_workbook('C:/python34/database/2015년.xls')
        break
    elif choice == 0:
        break    
    else :
        print("###다시 입력해주세요###")

i=0
while i < wb.nsheets:
    sh = wb.sheet_by_index(i)
    print(sh.name, sh.nrows, sh.ncols)
    a0 = ((str(sh.cell(2,6)).split("'"))[1])[:4]
    a01 = str(sh.cell(0,0)).split()
    a1 = str(a01[1]).split('월')
    a2 = str(sh.cell(7,6)).split(':')
    a3 = str(sh.cell(9,6)).split(':')
    a4 = str(sh.cell(10,6)).split(':')
    a5 = str(sh.cell(14,6)).split(':')
    a6 = str(sh.cell(15,6)).split(':')
    a7 = str(sh.cell(17,6)).split(':')
    a8 = str(sh.cell(21,6)).split(':')
    a9 = str(sh.cell(23,6)).split(':')
    a10 = str(sh.cell(25,6)).split(':')
    a11 = str(sh.cell(27,6)).split(':')
    a12 = str(sh.cell(29,6)).split(':')
    a13 = str(sh.cell(31,6)).split(':')
    a14 = str(sh.cell(33,6)).split(':')
    a15 = str(sh.cell(35,6)).split(':')
    a16 = str(sh.cell(37,6)).split(':')

    if choice == 2010 or choice == 2011 or choice == 2012 or choice == 2013:
        cur.execute("insert into jejutourist values (?,?,?,?,?,\
                                        ?,?,?,?,?,\
                                        ?,?,?,?,?,\
                                        ?,?,?,?)", 
                (str(a0[1]), float(a1[0]),float(a2[1]), float(a3[1]), float(a4[1]),\
                 float(a5[1]), float(a6[1]), float(a7[1]), float(a8[1]), float(a9[1]),\
                 float(a10[1]), float(a11[1]), float(a12[1]), float(a13[1]), float(a14[1]),\
                 float(a15[1]), float(a16[1]), 0, 0
                 ))
    elif choice == 2014 or choice == 2015:
        a17 = str(sh.cell(39,6)).split(':')
        a18 = str(sh.cell(41,6)).split(':')
        cur.execute("insert into jejutourist values (?,?,?,?,?,\
                                        ?,?,?,?,?,\
                                        ?,?,?,?,?,\
                                        ?,?,?,?)", 
                (str(a0[1]), float(a1[0]),float(a2[1]), float(a3[1]), float(a4[1]),\
                 float(a5[1]), float(a6[1]), float(a7[1]), float(a8[1]), float(a9[1]),\
                 float(a10[1]), float(a11[1]), float(a12[1]), float(a13[1]), float(a14[1]),\
                 float(a15[1]), float(a16[1]), float(a17[1]), float(a18[1])
                 ))
    i = i+1
        
#con.commit()

def print_menu():
        print('1. 일본')
        print('2. 중국')
        print('3. 홍콩')
        print('4. 대만')
        print('5. 싱가폴')
        print('6. 말레이시아')
        print('7. 아시아 기타')
        print('8. 미국')
        print('9. 서구권 기타')
        print('10. 인도네시아')
        print('11. 베트남')        
        print()

def create_graph():
        data= cur.fetchall()
        x, y =[],[]
        for line in data:
            x.append(line[0])
            y.append(line[1])

        plt.plot(x,y,linestyle='-', marker='o', label="value")

        plt.title(a)
        plt.xlabel("month")
        plt.ylabel("visitors")

        plt.autoscale(tight=True)
        plt.grid()
        plt.show()        
    

print_menu()
menu_choice = int(input("나라 선택(1-11) : "))
if menu_choice == 1:
    print("###일본 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_japan FROM jejutourist GROUP BY month")
    a = str('japan')
    create_graph()
    print()
elif menu_choice == 2:
    print("###중국 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_china FROM jejutourist GROUP BY month")
    a = str('china')
    create_graph()
    print()
elif menu_choice == 3:
    print("###홍콩 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_hongkong FROM jejutourist GROUP BY month")
    a = str('hongkong')
    create_graph()
    print()
elif menu_choice == 4:
    print("###대만 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_taiwan FROM jejutourist GROUP BY month")
    a = str('taiwan')
    create_graph()
    print()
elif menu_choice == 5:
    print("###싱가폴 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_singapore FROM jejutourist GROUP BY month")
    a = str('singapore')
    create_graph()
    print()
elif menu_choice == 6:
    print("###말레이시아 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_malasia FROM jejutourist GROUP BY month")
    a = str('malasia')
    create_graph()
    print()
elif menu_choice == 7:
    print("###아시아 기타 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_asia_etc FROM jejutourist GROUP BY month")
    a = str('asia_etc')
    create_graph()
    print()
elif menu_choice == 8:
    print("###미국 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_usa FROM jejutourist GROUP BY month")
    a = str('usa')
    create_graph()
    print()
elif menu_choice == 9:
    print("###서구권 기타 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_etc FROM jejutourist GROUP BY month")
    a = str('etc')
    create_graph()
    print()
elif menu_choice == 10:
    print("###인도네시아 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_indonesia FROM jejutourist GROUP BY month")
    a = str('indonesia')
    create_graph()
    print()
elif menu_choice == 11:
    print("###베트남 관광객 월별 그래프 보기###")
    cur.execute("SELECT month,f_vietnam FROM jejutourist GROUP BY month")
    a = str('vietnam')
    create_graph()
    print() 
