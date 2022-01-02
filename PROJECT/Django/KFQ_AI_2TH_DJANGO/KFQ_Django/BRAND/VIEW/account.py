from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from CRM.models import Member
from datetime import datetime
from CRM.models import ClassList, Member
from BRAND import views

class Account:

    def signup(request):
        context = None
        #진행중인 과정 SELECT
        classList = ClassList.objects.all()
        list = []
        for object in classList:
            #과정이 진행중인 반만 출력하기
            if object.status == '진행중':
                object.open_date = datetime.strftime(object.open_date,'%Y-%m-%d')
                object.close_date = datetime.strftime(object.close_date,'%Y-%m-%d')
                list.append(object)
        context = {
            'list' : list,
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
            class_fk = request.POST.get('class_fk')
            if password != repassword:
                messages.error(request, '비밀번호가 일치 하지 않습니다.')
                return HttpResponseRedirect('/BRAND/signup/')
            elif password is None or password.strip() == ''or email is None or email.strip() == '':
                messages.error(request, '필수 사항을 입력하세요.')
                return HttpResponseRedirect('/BRAND/signup/')
            elif password is None or password.strip() == '':
                messages.error(request, '비밀번호를 입력하세요.')
                return HttpResponseRedirect('/BRAND/signup/')
            elif email is None or email.strip() == '':
                messages.error(request, '이메일을 입력하세요.')
                return HttpResponseRedirect('/BRAND/signup/')
            else:
                user = Member.objects.create( name=name,birth=birth, email=email, password=password,
                                address=address, university=university, major= major ,interest_language=interest_language
                                ,authority=authority,phone_number=phone_number,class_fk_id=class_fk)
                user.save()
                return HttpResponseRedirect('/BRAND/signin/')
        
        return render(request, './brand/1_index.html', context)


    def signin(request):
        if request.method == 'POST':
        # 회원정보 조회
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = Member.objects.get(email=email, password=password)
                class_name = ClassList.objects.get(class_id=user.class_fk_id)
                print("hi",class_name)
                request.session['name'] = user.name
                request.session['birth'] = str(user.birth)
                request.session['email'] = user.email
                request.session['address'] = user.address
                request.session['university'] = user.university
                request.session['major'] = user.major
                request.session['interest_language'] = user.interest_language
                request.session['authority'] = user.authority
                request.session['phone_number'] = user.phone_number
                request.session['class_fk'] = user.class_fk_id
                request.session['class_name'] = class_name.class_name

                return render(request, './brand/1_index.html')
            except:
                return render(request, './brand/1_index.html')
        return render(request, './brand/1_index.html')

    def signout(request):
        del request.session['email'] # 개별 삭제
        request.session.flush() # 전체 삭제

        return HttpResponseRedirect('../index')

    def find_password(request):
        if request.method == "POST":
            inputPhonenumber = request.POST.get("phone_number")
            email = request.POST.get('email')
            name = request.POST.get('name')
            if inputPhonenumber is None or inputPhonenumber.strip() == '' or email is None or email.strip() == ''or name is None or name.strip() == '':
                messages.error(request,"정보를 다 입력해주세요." )
                return HttpResponseRedirect('/BRAND/find_password/')
            user = Member.objects.get(email=email)
            if inputPhonenumber == user.phone_number and email == user.email and name == user.name:
                messages.success(request,"비밀 번호는" + user.password + "입니다.")
                return HttpResponseRedirect('/BRAND/find_password/')
            else:
                messages.error(request,"정보를 다시 확인해주세요." )
                return HttpResponseRedirect('/BRAND/find_password/')
        return render(request, "./brand/page/02_account/find_password.html")