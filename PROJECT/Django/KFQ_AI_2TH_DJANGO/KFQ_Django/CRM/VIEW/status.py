from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import sqlite3
from CRM.models import ClassList, Member, Student_list
from datetime import timedelta, date, time, datetime
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.dateparse import parse_datetime
from CRM.forms import NoviceForm, UserForm
from django.forms.models import model_to_dict
from django.http import JsonResponse # JSON 응답


class Status :
    def status(request):
        print("PAGE : status")
        page ='status'
        
        classlist = ClassList.objects.all()
        list_name = []
        list_date = []

        list_attendance = []
        list_late = []
        list_early = []
        list_absent = []

        list_input_time = []
        list_output_time = []
        list_total_time = []
        list_temperature = []

        list_data=[]

        list_class_filter = 0

        if request.method == "POST":
            click_search = request.POST.get('ajax_class_name')

            for object in classlist:
                if object.class_name == click_search:
                    list_class_filter = object.class_id

        list_status = Student_list.objects.filter(class_fk=list_class_filter)
        context = {'classlist' : classlist,}
        for object in list_status:
            if list_class_filter  == object.member_fk.class_fk_id:
                list_name.append(object.member_fk)
                if object.date and object.output_time:
                    object.date = object.date.strftime('%Y-%m-%d')
                    object.input_time = object.input_time.strftime('%H:%M:%S')
                    object.output_time = object.output_time.strftime('%H:%M:%S')
                    #object.attandance = object.output_time.strftime('%H:%M:%S')
                    #object.absent = object.output_time.strftime('%H:%M:%S')
                   #bject.late = object.output_time.strftime('%H:%M:%S')
                   #bject.early = object.output_time.strftime('%H:%M:%S')
                    object.total_time = Status.diff_time(object.output_time, object.input_time)
                    object.absent = Status.check_status(object.input_time, object.output_time)
                elif object.input_time and not object.output_time:
                    object.date = object.date.strftime('%Y-%m-%d')
                    object.input_time = object.input_time.strftime('%H:%M:%S')
                    object.absent = '미퇴실'
                else:
                    object.absent = '결석'
            
            #dict_date = model_to_dict(object.date)
            #dict_input_time  = model_to_dict(object.input_time)
            #dict_output_time = model_to_dict(object.output_time)
            #dict_total_time  = model_to_dict(object.total_time)
            #dict_absent = model_to_dict(object.absent)

            #list_date.append(dict_date)
            #list_input_time.append(dict_input_time)
            #list_output_time.append(dict_output_time)
            #list_total_time.append(dict_output_time)
            #list_absent.append(dict_absent)
            #list_data.append(object)

            context = {'list_status' : list_status,'list_date' : list_date,'list_input_time' : list_input_time,'list_output_time' : list_output_time,'classlist' : classlist,}
        return render(request, './crm/03_status.html', context)
    
    def diff_time(time_in,time_out):
        t2 = datetime.strptime(time_out,'%H:%M:%S')
        t1 = datetime.strptime(time_in,'%H:%M:%S')
        time_stay = abs(t2-t1)
        result = time(time_stay.seconds //3600, (time_stay.seconds // 60) % 60).strftime('%H:%M')
        return result

    def check_status(time_in, time_out):

        standard_time = datetime.strptime('09:39:59','%H:%M:%S')
        t1 = datetime.strptime(time_in,'%H:%M:%S')
        t2 = datetime.strptime(time_out,'%H:%M:%S')
        
        diff_time = standard_time - t1


        time_stay = t2-t1
        time_stay= time_stay.seconds //3600
        result = ''


        if diff_time.days < 0 and time_stay > 5:
            result = '지각'
            return result
        elif time_stay < 7:
            result = '조퇴'
            return result
        else:
            result = '출석'
            return result

    def addnovice(request):
        print("PAGE : add_novice")

        if request.method == "POST":

            newbie_name = request.POST.get('name')

            newbie_birth = request.POST.get('birth')
            newbie_email = request.POST.get('email')
            newbie_digits = request.POST.get('digits')
            newbie_address = request.POST.get('address')
            newbie_univ = request.POST.get('univ')
            newbie_major = request.POST.get('major')
            newbie_language = request.POST.get('language')


            newbie = Member.objects.create(email=newbie_email,
                class_fk_id=1,
                name=newbie_name,age = '28',university=newbie_univ,major=newbie_major,
                interest_language=newbie_language, phone_number=newbie_digits, address=newbie_address,
                birth=newbie_birth, seat_num=1, authority='수강생')
            newbie.save()

        return render(request, './crm/page/account/add_novice.html')

    def signup(request):
        print("PAGE : status")
        page ='status'
        classlist = ClassList.objects.all()
        context = {
            'classlist' : classlist,
            'page':page,
        }

        if request.method == 'POST':
        # 회원정보 저장
            name = request.POST.get('name')
            birth = request.POST.get('birth')
            email = request.POST.get('email')
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            address = request.POST.get('address')
            university = request.POST.get('university')
            major = request.POST.get('major')
            interest_language = request.POST.get('interest_language')
            authority = request.POST.get('authority')
            phone_number = request.POST.get('phone_number')
            if password != repassword:
                messages.error(request, '비밀번호가 일치 하지 않습니다.')
            elif password is None or password.strip() == ''or email is None or email.strip() == '':
                messages.error(request, '필수 사항을 입력하세요.')
            elif password is None or password.strip() == '':
                messages.error(request, '비밀번호를 입력하세요.')
            elif email is None or email.strip() == '':
                messages.error(request, '이메일을 입력하세요.')
            else:
                user = Member.objects.create( name=name,birth=birth, email=email, password=password,
                                address=address, university=university, major= major ,interest_language=interest_language
                                ,authority=authority,phone_number=phone_number)
                user.save()
                return HttpResponseRedirect('#')
        return redirect('CRM:status')

    def stillhere(request):
        classlist = ClassList.objects.all()
        list_status_here = Student_list.objects.filter(attendance='Y')
        context = {'classlist' : classlist,}

        for object in list_status_here:
            object.date = object.date.strftime('%Y-%m-%d')
            object.input_time = object.input_time.strftime('%H:%M:%S')
            object.output_time = object.output_time.strftime('%H:%M:%S')
            object.total_time = Status.diff_time(object.output_time, object.input_time)
            object.absent = '미퇴실'
        context = {'list_status' : list_status_here, 'classlist' : classlist,}
        
        return render(request, './crm/page/03_status/status_02.html', context)

    def absent(request):
        classlist = ClassList.objects.all()
        list_status_here = Student_list.objects.filter(absent='Y')
        context = {'classlist' : classlist,}

        for object in list_status_here:
            object.date = ''
            object.input_time = ''
            object.output_time = ''
            object.total_time = '00:00'
            object.absent = '결석'

        
        context = {'list_status' : list_status_here, 'classlist' : classlist,}
        return render(request, './crm/page/03_status/status_03.html', context)

    def late(request):
        classlist = ClassList.objects.all()
        list_status_here = Student_list.objects.filter(late='Y')
        context = {'classlist' : classlist,}

        for object in list_status_here:
            object.date = object.date.strftime('%Y-%m-%d')
            object.input_time = object.input_time.strftime('%H:%M:%S')
            object.output_time = object.output_time.strftime('%H:%M:%S')
            object.total_time = Status.diff_time(object.output_time, object.input_time)
            object.absent = '지각'
        context = {'list_status' : list_status_here, 'classlist' : classlist,}
        return render(request, './crm/page/03_status/status_04.html', context)


    
    def early(request):
        classlist = ClassList.objects.all()
        list_status_here = Student_list.objects.filter(early='Y')
        context = {'classlist' : classlist,}

        for object in list_status_here:
            object.date = object.date.strftime('%Y-%m-%d')
            object.input_time = object.input_time.strftime('%H:%M:%S')
            object.output_time = object.output_time.strftime('%H:%M:%S')
            object.total_time = Status.diff_time(object.output_time, object.input_time)
            object.absent = '조퇴'
        context = {'list_status' : list_status_here, 'classlist' : classlist,}
        return render(request, './crm/page/03_status/status_05.html', context)
        

#***********************************************************************#    