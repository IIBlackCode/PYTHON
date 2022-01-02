from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render
from datetime import timedelta, date, time, datetime
import sqlite3
#***********************************************************************#
# Dashboard 통계
conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
cur = conn.cursor()
currentTime = datetime.now().strftime('%Y-%m-%d')

class Dashboard :
    #진행중인 총 수강생의 수
    def total_member(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        print("=========================",currentTime)
        with conn:
            cur.execute("select count(*) from CRM_member ")
            total = cur.fetchone()
            print('총 수강생 수 : ',total[0])
        with conn:
            querry = "select count(*) from CRM_student_list WHERE attendance like 'Y' AND date = "
            cur.execute(querry + '\''+currentTime+'\'')
            attendance = cur.fetchone()
            print('1. 출석 수 : ',attendance[0])
        with conn:
            querry = "select count(*) from CRM_student_list WHERE absent like 'Y' AND date = "
            cur.execute(querry + '\''+currentTime+'\'')
            absent = cur.fetchone()
            print('2. 결석 수 : ',absent[0])
        with conn:
            querry = "select count(*) from CRM_student_list WHERE late like 'Y' AND date = "
            cur.execute(querry + '\''+currentTime+'\'')
            late = cur.fetchone()
            print('3. 지각 수 : ',late[0])
        with conn:
            querry = "select count(*) from CRM_student_list WHERE early like 'Y' AND date = "
            cur.execute(querry + '\''+currentTime+'\'')
            early = cur.fetchone()
            print('4. 조퇴 수 : ',early[0])
        context = {
            'total' : total[0],
            'attendance' : attendance[0],
            'absent' : absent[0],
            'late' : late[0],
            'early' : early[0],
        }
        return JsonResponse(context,status=200)
        # return render(request, './crm/page/01_index/index_01.html', context)

    #총 출석 수
    def total_attendance(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select count(*) from CRM_student_list WHERE attendance like 'Y' ")
        count = cur.fetchone()
        print('출석 수 : ',count[0])
            
        return JsonResponse({'count' :count[0]},status=200)

    #총 결석 수
    def total_absent(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select count(*) from CRM_student_list WHERE absent like 'Y' ")
        count = cur.fetchone()
        print('결석 수 : ',count[0])
            
        return JsonResponse({'count' :count[0]},status=200)

    #총 지각 수
    def total_late(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select count(*) from CRM_student_list WHERE late like 'Y' ")
        count = cur.fetchone()
        print('지각 수 : ',count[0])
            
        return JsonResponse({'count' :count[0]},status=200)

    #총 조퇴 수
    def total_early(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select count(*) from CRM_student_list WHERE early like 'Y' ")
        count = cur.fetchone()
        print('조퇴 수 : ',count[0])
            
        return JsonResponse({'count' :count[0]},status=200)


    def class_statistics(request):
        class_fk = request.GET.get('class_fk')
        print('class_fk :',str(class_fk))
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        with conn:
            querry = "select count(*) from CRM_student_list t1, CRM_member t2 WHERE t1.member_fk_id = t2.email AND t1.attendance like 'Y' AND t2.class_fk_id ="+class_fk+" AND t1.date = "+'\''+currentTime+'\''
            cur.execute(querry)
            attendance = cur.fetchone()
            print('반 출석 수 : ',attendance[0])
        with conn:
            querry = "select count(*) from CRM_student_list t1, CRM_member t2 WHERE t1.member_fk_id = t2.email AND t1.absent like 'Y' AND t2.class_fk_id ="+class_fk+" AND t1.date = "+'\''+currentTime+'\''
            cur.execute(querry)
            absent = cur.fetchone()
            print('반 결석 수 : ',absent[0])
        with conn:
            querry = "select count(*) from CRM_student_list t1, CRM_member t2 WHERE t1.member_fk_id = t2.email AND t1.late like 'Y' AND t2.class_fk_id ="+class_fk+" AND t1.date = "+'\''+currentTime+'\''
            cur.execute(querry)
            late = cur.fetchone()
            print('반 지각 수 : ',late[0])
        with conn:
            querry = "select count(*) from CRM_student_list t1, CRM_member t2 WHERE t1.member_fk_id = t2.email AND t1.early like 'Y' AND t2.class_fk_id ="+class_fk+" AND t1.date = "+'\''+currentTime+'\''
            cur.execute(querry)
            early = cur.fetchone()
            print('반 조퇴 수 : ',early[0])
        with conn:
            querry = "select count(*) from CRM_member WHERE class_fk_id ="+class_fk+" "
            
            cur.execute(querry)
            totalCountMember = cur.fetchone()
            print('반 인원 수 : ',totalCountMember[0])

        context = {
            'attendance':attendance,
            'absent':absent,
            'late':late,
            'early':early,
            'totalCountMember':totalCountMember,
        }
        return JsonResponse({'context' :context},status=200)

    def classNameList(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select class_name from CRM_classlist WHERE status like '진행중' ")
        classNameList = cur.fetchall()
        print('진행과정 : ',classNameList)
            
        return JsonResponse({'count' :classNameList},status=200)

    #과정 진행율
    def process(request):
        conn = sqlite3.connect("db.sqlite3",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select class_name,(julianday(Date('now'))-julianday(open_date))/(julianday(close_date)-julianday(open_date))*100 from CRM_classlist WHERE status like '진행중' ")
        data = cur.fetchall()
        print('진행율 : ',data)
            
        return JsonResponse({'data' :data},status=200)
    