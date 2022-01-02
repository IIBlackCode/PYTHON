from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from CRM.models import Member
from datetime import datetime
from CRM.models import ClassList, Member

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
                return HttpResponseRedirect('/CRM/signup/')
            elif password is None or password.strip() == ''or email is None or email.strip() == '':
                messages.error(request, '필수 사항을 입력하세요.')
                return HttpResponseRedirect('/CRM/signup/')
            elif password is None or password.strip() == '':
                messages.error(request, '비밀번호를 입력하세요.')
                return HttpResponseRedirect('/CRM/signup/')
            elif email is None or email.strip() == '':
                messages.error(request, '이메일을 입력하세요.')
                return HttpResponseRedirect('/CRM/signup/')
            else:
                user = Member.objects.create( name=name,birth=birth, email=email, password=password,
                                address=address, university=university, major= major ,interest_language=interest_language
                                ,authority=authority,phone_number=phone_number,class_fk_id=class_fk)
                user.save()
                return HttpResponseRedirect('/CRM/signin/')
        
        return render(request, './crm/page/02_account/signup.html', context)


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
                session_list = ['name','birth','email','address','university','major',
                                'interest_language','authority','phone_number',
                                'class_fk', 'class_name', ]
                for i in session_list:
                    if request.session[i] is None:
                        request.session[i] = ""

                return render(request, './crm/page/02_account/signin_success.html')
            except:
                return render(request, './crm/page/02_account/signin_fail.html')
        return render(request, './crm/page/02_account/signin.html')

    def signout(request):
        del request.session['email'] # 개별 삭제
        request.session.flush() # 전체 삭제

        return HttpResponseRedirect('/CRM/signin/')
        # return HttpResponseRedirect('/CRM/signin/')


    def change_pw(request):
        
        if request.method == "POST":
            # 현재 html 창에서 비밀번호 호출
            input_password = request.POST.get("password")
            password1=request.POST.get("password1")
            password2=request.POST.get("password2")
            email=request.session['email']
            user = Member.objects.get(email=email)
            # 입력한 비밀번호가 기존의 비밀번호와 같은 경우
            if input_password == user.password:
                if  password1==password2:
                    user.password = password1
                    user.save()
                    messages.success(request,"비밀 번호가 변경되었습니다.")
                    return render(request, "CRM/02_settings.html",)
                elif password1 is None or password1.strip() == ''or password2 is None or password2.strip() == '':
                    messages.error(request, '비밀번호를 입력하세요.')
                elif password1!=password2:
                    # 새로운 비밀 번호가 일치 하지 않습니다.
                    messages.error(request, '새로운 비밀번호가 일치 하지 않습니다.')
                    return HttpResponseRedirect('/CRM/settings/')
                return HttpResponseRedirect('/CRM/settings/')
            # 입력한 비밀 번호가 기존의 비밀 번호와 다른 경우
            elif input_password != user.password:
                # 비밀 번호를 확인해주세요
                messages.error(request, '현재 비밀 번호를 확인해주세요')
                return HttpResponseRedirect('/CRM/settings/')
        else:
            messages.error(request, '비밀 번호를 확인해주세요')
        return render(request, "CRM/02_settings.html")
            
            
    def change_info(request):

        if request.method == "POST":
            email=request.session['email']
            user = Member.objects.get(email=email)
            inputPhonenumber = request.POST.get("inputPhonenumber")
            inputAddress = request.POST.get("inputAddress")
            inputUniv = request.POST.get("inputUniv")
            inputMajor = request.POST.get("inputMajor")
            inputLanguage = request.POST.get("inputLanguage")
            user.phone_number = inputPhonenumber
            user.address = inputAddress
            user.university = inputUniv
            user.major = inputMajor
            user.interest_language = inputLanguage
            user.save()

            request.session['phone_number'] = user.phone_number
            request.session['address'] = user.address
            request.session['university'] = user.university
            request.session['major'] = user.major
            request.session['interest_language'] = user.interest_language
            
            return render(request, "CRM/02_settings.html")
        return render(request, "CRM/02_settings.html")



    def delete_member(request):
        
        if request.method == "POST":

            email=request.session['email']
            user = Member.objects.get(email=email)
            user.delete()
            del request.session['email'] # 개별 삭제
            request.session.flush() # 전체 삭제
            return redirect('/CRM/signin/')

    def find_password(request):
        if request.method == "POST":
            inputPhonenumber = request.POST.get("phone_number")
            email = request.POST.get('email')
            name = request.POST.get('name')
            if inputPhonenumber is None or inputPhonenumber.strip() == '' or email is None or email.strip() == ''or name is None or name.strip() == '':
                messages.error(request,"정보를 다 입력해주세요." )
                return HttpResponseRedirect('/CRM/signin/find_password/')
            user = Member.objects.get(email=email)
            if inputPhonenumber == user.phone_number and email == user.email and name == user.name:
                messages.success(request,"비밀 번호는" + user.password + "입니다.")
                return HttpResponseRedirect('/CRM/signin/find_password/')
            else:
                messages.error(request,"정보를 다시 확인해주세요." )
                return HttpResponseRedirect('/CRM/signin/find_password/')
        return render(request, "./crm/page/02_account/find_password.html")