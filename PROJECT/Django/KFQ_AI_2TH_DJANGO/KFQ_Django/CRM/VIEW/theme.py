from django.http import HttpResponse
from django.shortcuts import render
#***********************************************************************#
# Original Theme
class Theme :
    def theme_index(request):
        print("PAGE : theme_index")
        page ='Dashboard'
        context = {
            'page' : page
        }
        return render(request, './theme/01_index.html', context)

    def theme_profile(request):
        print("PAGE : theme_profile")
        page ='Profile'
        context = {
            'page' : page
        }
        return render(request, './theme/02_profile.html', context)

    def theme_settings(request):
        print("PAGE : theme_settings")
        page ='Settings'
        context = {
            'page' : page
        }
        return render(request, './theme/03_settings.html', context)

    def theme_invoice(request):
        print("PAGE : theme_invoice")
        page ='Invoice'
        context = {
            'page' : page
        }
        return render(request, './theme/04_invoice.html', context)

    def theme_blank(request):
        print("PAGE : theme_blank")
        page ='Blank'
        context = {
            'page' : page
        }
        return render(request, './theme/05_blank.html', context)

    def theme_UI_Element(request, page):
        print("PAGE : ",page)

        context = {
            'page' : page
        }
        if page == "01-alerts.html":
            return render(request, './theme/UI_Element/ui-alerts.html', context)
        elif page == "02-buttons.html":
            return render(request, './theme/UI_Element/ui-buttons.html', context)
        elif page == "03-cards.html":
            return render(request, './theme/UI_Element/ui-cards.html', context)
        elif page == "04-general.html":
            return render(request, './theme/UI_Element/ui-general.html', context)
        elif page == "05-grid.html":
            return render(request, './theme/UI_Element/ui-grid.html', context)
        elif page == "06-modals.html":
            return render(request, './theme/UI_Element/ui-modals.html', context)
        elif page == "07-typography.html":
            return render(request, './theme/UI_Element/ui-typography.html', context)

        return render(request, './theme/06_UI_Element.html', context)

    def theme_icons(request):
        print("PAGE : theme_icons")
        page ='Icons'
        context = {
            'page' : page
        }
        return render(request, './theme/07_icons.html', context)

    def theme_Forms(request, page):
        print("PAGE : theme_Forms",page)

        context = {
            'page' : page
        }
        if page == "01-layouts.html":
            return render(request, './theme/Forms/'+page, context)
        elif page == "02-basic-inputs.html":
            return render(request, './theme/Forms/'+page, context)

    def theme_tables(request):
        print("PAGE : theme_tables")
        page ='Tables'
        context = {
            'page' : page
        }
        return render(request, './theme/09_tables.html', context)

    def theme_chart(request):
        print("PAGE : theme_Charts")
        page ='Charts'
        context = {
            'page' : page
        }
        return render(request, './theme/10_charts.html', context)

    def theme_maps(request):
        print("PAGE : theme_maps")
        page ='Maps'
        context = {
            'page' : page
        }
        return render(request, './theme/11_maps.html', context)
#***********************************************************************#