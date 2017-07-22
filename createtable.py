import sqlite3
import xlrd
import xlsxwriter
import math

con = sqlite3.connect("testDB")
cur = con.cursor()

wb = xlrd.open_workbook('C:/python34/database/2010년.xls')
print("The number of worksheets is", wb.nsheets)
print("Worksheet name(s):", wb.sheet_names())
cur.execute("delete from jejutourist")

i=0
while i < wb.nsheets:
    sh = wb.sheet_by_index(i)
    print(sh.name, sh.nrows, sh.ncols)
    cur.execute("insert into jejutourist values (?,?,?,?,?,\
                                           ?,?,?,?,?,\
                                           ?,?,?,?,?,\
                                           ?,?,?,?)", 
#               (((str(sh.cell(2,6))).split(':'))[1],\
#엑셀에서 (2,6) cell의 값이 sheet에 따라 다르게 작성됨; 
#그래서, 2,6) cell의 값을 모두 프린트해서 본 후 년도만 추출하는 방안을 마련함 
#프로그램 아래 부분에서 프린트 결과 참고 
                ((((str(sh.cell(2,6))).split("'"))[1])[:4],\
                 (((str(sh.cell(0,0))).split())[1]).rstrip("월"),\
                 ((str(sh.cell(7,6))).split(":"))[1],\
                 ((str(sh.cell(9,6))).split(":"))[1],\
                 ((str(sh.cell(20,6))).split(":"))[1],\
                 ((str(sh.cell(22,6))).split(":"))[1],\
                 ((str(sh.cell(24,6))).split(":"))[1],\
                 ((str(sh.cell(26,6))).split(":"))[1],\
                 ((str(sh.cell(28,6))).split(":"))[1],\
                 ((str(sh.cell(30,6))).split(":"))[1],\
                 ((str(sh.cell(34,6))).split(":"))[1],\
                 ((str(sh.cell(36,6))).split(":"))[1],\
                 ((str(sh.cell(38,6))).split(":"))[1],\
                 ((str(sh.cell(40,6))).split(":"))[1],\
                 ((str(sh.cell(42,6))).split(":"))[1],\
                 ((str(sh.cell(44,6))).split(":"))[1],\
                 ((str(sh.cell(46,6))).split(":"))[1],\
                 ((str(sh.cell(48,6))).split(":"))[1],\
                 ((str(sh.cell(50,6))).split(":"))[1]
                ))
    i = i+1    
con.commit()

print("----------------------------------------------------------------")
for row in cur.execute("select * from jejutourist;"):
    print(row)

print("----------------------------------------------------------------")
for row in cur.execute("select sum(d_individual), sum(d_group), sum(d_leisure) as dum_of_d_group from jejutourist;"):
    print("sum(d_individual), sum(d_group), sum(d_leisure)")
    print(row)

print("----------------------------------------------------------------")
print("month, sum(d_individual), sum(d_group), sum(d_leisure)")
for row in cur.execute("select month, sum(d_individual), sum(d_group), sum(d_leisure) as dum_of_d_group \
                        from jejutourist\
                        group by month\
                        order by month;"):
    print(row)

print("----------------------------------------------------------------")
print("Japan -- China -- Hongkong -- Twiwan -- Singapore -- Malasia -- Asia_etc -- USA -- etc")
for row in cur.execute("select month, sum(f_japan), sum(f_china), sum(f_hongkong), 				sum(f_taiwan), sum(f_singapore), \
                        	sum(f_malasia), sum(f_asia_etc), sum(f_usa),\
				sum(f_etc) as dum_of_d_group \
                        from jejutourist\
                        group by month\
                        order by month;"):
    print(row)
