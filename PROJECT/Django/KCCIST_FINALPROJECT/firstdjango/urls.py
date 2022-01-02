"""
urls.py 역할
사이트의 url규칙 리스팅

firstdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#first 패키지 내에 있는 view 파이썬 파일 import

#path, include
from django.urls import path, include

urlpatterns = [
    #path('', views.index, name='index'),
    #first패키이 내에 urls 참조하는 방식으로 변경
    path('', include('project_bigdata.urls')),
    path('admin/', admin.site.urls),
]
