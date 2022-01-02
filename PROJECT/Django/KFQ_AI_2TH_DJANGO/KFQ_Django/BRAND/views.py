from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("BRAND PAGE.")
#***********************************************************************#
class Brand :
    def index(request):
        print("PAGE : theme_index")
        page ='Home'
        context = {
            'page' : page
        }
        return render(request, './brand/1_index.html', context)

    def aboutus(request):
        print("PAGE : theme_about")
        page = 'About Us'
        context = {
            'page': page
        }
        return render(request, './brand/2_about.html', context)

    def features(request):
        print("PAGE : theme_features")
        page = 'Features'
        context = {
            'page': page
        }
        return render(request, './brand/3_features.html', context)

    def hosting(request):
        print("PAGE : theme_hosting")
        page = 'Hosting'
        context = {
            'page': page
        }
        return render(request, './brand/4_hosting.html', context)

    def domain(request):
        print("PAGE : theme_domain")
        page = 'Domain'
        context = {
            'page': page
        }
        return render(request, './brand/5_domain.html', context)

    def pricing(request):
        print("PAGE : theme_domain")
        page = 'Pricing'
        context = {
            'page': page
        }
        return render(request, './brand/6_pricing.html', context)

    def contact(request):
        print("PAGE : theme_contact")
        page = 'Contact'
        context = {
            'page': page
        }
        return render(request, './brand/7_contact.html', context)
#***********************************************************************#
