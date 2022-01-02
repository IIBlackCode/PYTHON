from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
import sqlite3
from CRM.models import ClassList, Member, Student_list
from datetime import timedelta, date, time, datetime
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.dateparse import parse_datetime
from CRM.forms import NoviceForm, UserForm
from django.contrib import messages

# Create your views here.
def index(request):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    query = '''select * from KFQ_answer'''
    result = cur.execute(query)
    print("test",result.fetchall())
    return HttpResponse("CRM PAGE.")
    
#***********************************************************************#
class Crm :
    def index(request):
        print("PAGE : index")
        page ='Dashboard'

        #진행중인 과정 SELECT
        classList = ClassList.objects.all()
        list = []
        prosessess = []
        try:
            for object in classList:
                #과정이 진행중인 반만 출력하기
                if object.status == '진행중':
                    totalDay = (object.close_date-object.open_date).days
                    processDay = (datetime.now().date()-object.open_date).days
                    process = int(processDay/totalDay*100)
                    print('진행도 : ',process)
                    prosessess.append(process)

                    object.open_date = datetime.strftime(object.open_date,'%Y-%m-%d')
                    object.close_date = datetime.strftime(object.close_date,'%Y-%m-%d')
                    list.append(object)
                   
        except:
            print("ClassList.objects.all() ---> Error!")

        #입실한 수강생 출결내역
        studentList = []
        objectList = Student_list.objects.all()

        #당일 출결 학생들만 출력
        currentTime = datetime.now().strftime('%Y-%m-%d')
        # print('currentTime',currentTime)
        try:
            for object in objectList:
                # object.date = datetime.strftime(object.date,'%Y-%m-%d')
                if currentTime == datetime.strftime(object.input_time,'%Y-%m-%d') :
                    # print('object.date',object.date)
                    studentList.append(object)
        except:
            print("Student_list.objects.all() Error! --> No Data")
            
        context = {
            'currentTime':datetime.now(),
            'page' : page,
            'list' : list,
            'studentList':studentList,
            'prosessess' :prosessess,
        }
        return render(request, './crm/01_index.html', context)
    def profile(request):
        print("PAGE : profile")
        page ='Profile'
        context = {
            'page' : page
        }
        return render(request, './crm/02_profile.html', context)
    def settings(request):
        print("PAGE : settings")
        page ='Settings'
        context = {
            'page' : page
        }
        return render(request, './crm/02_settings.html', context)
    
    def status(request):
        print("PAGE : status")
        classlist = ClassList.objects.all()
        page ='status'

        context = {
            'page' : page,
            'classlist' : classlist,
        }
        return render(request, './crm/03_status.html', context)

    def statistics(request):
        print("PAGE : statistics")
        page ='statistics'
        context = {
            'page' : page
        }
        return render(request, './crm/04_statistics.html', context)

    def seatingChart(request):
        print("PAGE : SeatingChart")
        page ='SeatingChart'
        context = {
            'page' : page
        }
        return render(request, './crm/05_seatingChart.html', context)


    def ui_Element(request, page):
        print("PAGE : ",page)

        context = {
            'page' : page
        }
        if page == "01-alerts.html":
            return render(request, './crm/Element/UI_Element/ui-alerts.html', context)
        elif page == "02-buttons.html":
            return render(request, './crm/Element/UI_Element/ui-buttons.html', context)
        elif page == "03-cards.html":
            return render(request, './crm/Element/UI_Element/ui-cards.html', context)
        elif page == "04-general.html":
            return render(request, './crm/Element/UI_Element/ui-general.html', context)
        elif page == "05-grid.html":
            return render(request, './crm/Element/UI_Element/ui-grid.html', context)
        elif page == "06-modals.html":
            return render(request, './crm/Element/UI_Element/ui-modals.html', context)
        elif page == "07-typography.html":
            return render(request, './crm/Element/UI_Element/ui-typography.html', context)

        # return render(request, './crm/Element/06_UI_Element.html', context)

    def icons(request):
        print("PAGE : theme_icons")
        page ='Icons'
        context = {
            'page' : page
        }
        return render(request, './crm/Element/07_icons.html', context)

    def forms(request, page):
        print("PAGE : theme_Forms",page)

        context = {
            'page' : page
        }
        if page == "01-layouts.html":
            return render(request, './crm/Element/Forms/'+page, context)
        elif page == "02-basic-inputs.html":
            return render(request, './crm/Element/Forms/'+page, context)

    def tables(request):
        print("PAGE : theme_tables")
        page ='Tables'
        context = {
            'page' : page
        }
        return render(request, './crm/Element/09_tables.html', context)

    def chart(request):
        print("PAGE : theme_Charts")
        page ='Charts'
        context = {
            'page' : page
        }
        return render(request, './crm/Element/10_charts.html', context)

    def maps(request):
        print("PAGE : theme_maps")
        page ='Maps'
        context = {
            'page' : page
        }
        return render(request, './crm/Element/11_maps.html', context)
#***********************************************************************#    