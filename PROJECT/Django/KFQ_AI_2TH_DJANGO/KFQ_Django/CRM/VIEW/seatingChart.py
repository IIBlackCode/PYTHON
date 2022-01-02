from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render
import sqlite3
#***********************************************************************#
# seatingChart
conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
cur = conn.cursor()

class SeatingChart :
    def seatingChart(request):
        class_fk = request.GET.get('class_fk')
        member_fk = request.GET.get('member_fk')
        print('class_fk :',str(class_fk))
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        with conn:
            cur.execute("select name from CRM_member t1 where t1.class_fk_id ="+class_fk+" order by t1.email")
            name = cur.fetchall()
        with conn:
            cur.execute("select major from CRM_member t1 where t1.class_fk_id ="+class_fk+" order by t1.email")
            major = cur.fetchall()
        with conn:
            cur.execute("select seat_num from CRM_member t1 where t1.class_fk_id ="+class_fk+" order by t1.email")
            seat_num = cur.fetchall()
        with conn:
            cur.execute("select max(t1.input_time),t1.temperature,t1.attendance,t1.absent,t1.late,t1.early from CRM_student_list t1, CRM_member t2 where t1.member_fk_id = t2.email and t2.class_fk_id ="+class_fk+" group by t1.member_fk_id order by t1.member_fk_id")
            daily_info = cur.fetchall()
        with conn:
            cur.execute("select class_name from CRM_member t1, CRM_classlist t2 where t1.class_fk_id = t2.class_id and t2.class_id="+class_fk)
            class_name = cur.fetchall()
        with conn:
            cur.execute("select t2.email from CRM_student_list t1, CRM_member t2, CRM_classlist t3 where t1.member_fk_id = t2.email and t2.class_fk_id ="+class_fk+" group by t1.member_fk_id order by t1.member_fk_id")
            email = cur.fetchall()
        context = {
            'name' :name,
            'major':major,
            'seat_num':seat_num,
            'daily_info':daily_info,
            'class_name':class_name,
            'email':email,
        }
        return JsonResponse({'context' :context},status=200)