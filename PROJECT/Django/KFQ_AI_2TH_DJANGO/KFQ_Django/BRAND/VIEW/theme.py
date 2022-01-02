from django.http import HttpResponse
from django.shortcuts import render

#***********************************************************************#
# Original Theme
class Theme :
    def theme_index(request):
        print("PAGE : theme_index")
        page ='Home'
        context = {
            'page' : page
        }
        return render(request, './Theme/1_index.html', context)

    def theme_aboutus(request):
        print("PAGE : theme_about")
        page = 'About Us'
        context = {
            'page': page
        }
        return render(request, './Theme/2_about.html', context)

    def theme_features(request):
        print("PAGE : theme_features")
        page = 'Features'
        context = {
            'page': page
        }
        return render(request, './Theme/3_features.html', context)

    def theme_hosting(request):
        print("PAGE : theme_hosting")
        page = 'Hosting'
        context = {
            'page': page
        }
        return render(request, './Theme/4_hosting.html', context)

    def theme_domain(request):
        print("PAGE : theme_domain")
        page = 'Domain'
        context = {
            'page': page
        }
        return render(request, './Theme/5_domain.html', context)

    def theme_pricing(request):
        print("PAGE : theme_domain")
        page = 'Pricing'
        context = {
            'page': page
        }
        return render(request, './Theme/6_pricing.html', context)

    def theme_contact(request):
        print("PAGE : theme_contact")
        page = 'Contact'
        context = {
            'page': page
        }
        return render(request, './Theme/7_contact.html', context)
#***********************************************************************#