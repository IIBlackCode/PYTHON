from django.urls import path
from CRM import views
from .VIEW.theme import Theme
from django.contrib.auth import views as auth_views
from .VIEW.account import Account
from .VIEW.dashboard import Dashboard
from .VIEW.QuerryTest import Test
from .VIEW.status import Status
from .VIEW.seatingChart import SeatingChart
from django.conf.urls import url
app_name='CRM'
urlpatterns = [
    path('test/', Test.test01),
    #***********************************************************************#
    #PAGE : 01_index Dashboard
    path('index/total_member/',             Dashboard.total_member,        name='total_member'),
    path('index/total_attendance/',         Dashboard.total_attendance,    name='Total_attendance'),
    path('index/total_absent/',             Dashboard.total_absent,        name='Total_attendance'),
    path('index/total_late/',               Dashboard.total_late,          name='Total_attendance'),
    path('index/total_early/',              Dashboard.total_early,         name='Total_attendance'),
    path('index/class_statistics/',         Dashboard.class_statistics,    name='class_statistics'),
    path('index/classNameList/',            Dashboard.classNameList,        name='class_statistics'),
    path('index/process/',                  Dashboard.process,              name='class_statistics'),
    #***********************************************************************#
    #PAGE : 02_Account
    path('signup/',                           Account.signup,           name='signup'),
    path('signin/',                           Account.signin,           name='signin'),
    path('signout/',                          Account.signout,          name='signout'),
    path('settings/password/',                Account.change_pw,        name='change_pw'),
    path('settings/info/',                    Account.change_info,      name='change_info'),
    path('settings/delete/',                  Account.delete_member,    name='delete_member'),
    path('signin/find_password/',             Account.find_password,    name='find_password'),
    #***********************************************************************#
    #PAGE : 03_status     
    path('status/data/',                    Status.status,        name='status_data'),
    path('add_novice/',                     Status.addnovice,     name='add_novice'),
    path('status/join/',                    Status.addnovice,     name='add_member'),
    path('status/data/stay/',               Status.stillhere,     name='status_stay'),
    path('status/data/late/',               Status.late,          name='status_late'),
    path('status/data/absent/',             Status.absent,        name='status_absent'),
    path('status/data/early/',              Status.early,         name='status_early'),
    #***********************************************************************#
    #PAGE : 05_seatingChart     
    path('seatingChart/seatingChart/',      SeatingChart.seatingChart,     name='seatingChart_data'),
    #***********************************************************************#
    path('index/',                          views.Crm.index,      name='index'),
    path('profile/',                        views.Crm.profile,    name='profile'),
    path('settings/',                       views.Crm.settings,   name='settings'),
    path('status/',                         views.Crm.status,     name='status'),
    path('statistics/',                     views.Crm.statistics, name='statics'),
    path('seatingChart/',                   views.Crm.seatingChart,    name='seatingChart'),
    path('UI_Element/page=<page>/',         views.Crm.ui_Element, name='UI_Element'),
    path('icons/',                          views.Crm.icons,      name='icons'),
    path('forms/page=<page>/',              views.Crm.forms,      name='Forms'),
    path('tables/',                         views.Crm.tables,     name='tables'),
    path('charts/',                         views.Crm.chart,      name='charts'),
    path('maps/',                           views.Crm.maps,       name='maps'),
#***********************************************************************#
    # Original Theme
    path('theme/index/',                    Theme.theme_index,      name='01_index.html'),
    path('theme/profile/',                  Theme.theme_profile,    name='02_profile.html'),
    path('theme/settings/',                 Theme.theme_settings,   name='03_settings.html'),
    path('theme/invoice/',                  Theme.theme_invoice,    name='04_invoice.html'),
    path('theme/blank/',                    Theme.theme_blank,      name='05_blank.html'),
    path('theme/UI_Element/page=<page>/',   Theme.theme_UI_Element, name='06_UI_Element.html'),
    path('theme/icons/',                    Theme.theme_icons,      name='07_icons.html'),
    path('theme/forms/page=<page>/',        Theme.theme_Forms,      name='08_Forms.html'),
    path('theme/tables/',                   Theme.theme_tables,     name='09_tables.html'),
    path('theme/charts/',                   Theme.theme_chart,      name='10_charts.html'),
    path('theme/maps/',                     Theme.theme_maps,       name='11_maps.html'),
    # path('theme//', views.index, name=''),
#***********************************************************************#
]