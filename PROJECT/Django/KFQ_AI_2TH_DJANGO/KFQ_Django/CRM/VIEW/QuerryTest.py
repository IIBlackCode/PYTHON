from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import datetime

# Create your views here.
class Test :
    def test01(request):
        conn = sqlite3.connect("db.sqlite3")
        
        with conn:
            cur = conn.cursor()
            cur.execute("select * from CRM_student_list")
            rows = cur.fetchall()
        
            for row in rows:
                print(row)

        with conn:
            cur = conn.cursor()
            cur.execute("select count(*) from CRM_member")
            rows = cur.fetchall()
        
            for row in rows:
                print(row)

        with conn:
            cur = conn.cursor()
            cur.execute("select count(*) from CRM_student_list WHERE late like 'Y' ")
            rows = cur.fetchall()
            print('결석 수 : ',rows)
            for row in rows:
                print(row)


        return HttpResponse("CRM PAGE.")

    def total_member(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()

        now = datetime.datetime.now()
        print(now) 

        
        cur.execute("select count(*) from CRM_member ")
        count = cur.fetchone()
        print('출석 수 : ',count[0])
        
        return HttpResponse("CRM PAGE."+str(count[0]))
        # return JsonResponse({'count' :count[0]},status=200)