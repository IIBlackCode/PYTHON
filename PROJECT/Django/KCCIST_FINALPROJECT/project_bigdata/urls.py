from django.urls import path
#from django.conf.urls import patterns, url
from . import views, viewsSimulator


urlpatterns = [
    path('',views.index, name='index'),
    #path('<word>/',viewsSimulator.radioTheme, name='radioTheme'),
    path('radioTheme/',views.radioTheme, name='radioTheme'),
    path('radioStock/',views.radioStock, name='radioStock'),
    path('radioTerm/',views.radioTerm, name='radioTerm'),
    path('radioData/',views.radioData, name='radioData'),
    path('radioModel/',views.radioModel, name='radioModel'),
    path('radioPredictDate/',views.radioPredictDate, name='radioPredictDate'),


    path('clkTrain/', views.ChartAPIView.as_view(), name="clkTrain"),
    # path('chart', viewsSimulator.ChartView.as_view(), name="chart"),
    path('saveModel/',views.saveModel, name='saveModel'),
    path('syncData/',views.syncData, name='syncData'),


    path('data_sync/',views.data_sync, name='data_sync'),
    path('elements/',views.elements, name='elements.html'),
    path('icons/',views.icons, name='icons.html'),
]