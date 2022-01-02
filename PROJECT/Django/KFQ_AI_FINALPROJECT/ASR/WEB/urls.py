"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from .view.ver1 import Ver1
from .view.server import View
from .view import server
# from .view.WebCamera import * 

urlpatterns = [
    
    # PAGE URL
    path('monitoring/<hw>/<dl>/',      View.server,         name='Ver1_dashboard'),
    
    # Web Camera URL
    path('WebCamera/<model>/',         View.webCamera,     name='Ver1_dashboard'),
    
    # Turtlebot Camera URL
    path('TurtlebotCamera/<model>/',   View.imageAPI_Client, name='Ver1_dashboard'),

    # Exception Message
    # path('exception/',                 server.exception_message, name='Ver1_dashboard'),

    # CSS, JS
    path('dashboard/index=<num>',      Ver1.dashboard,                 name='Ver1_dashboard'),
    path('apps/<app>/<email>',         Ver1.apps,         name='Ver1_dashboard'),
    path('charts/<chart>',             Ver1.chart,         name='Ver1_dashboard'),
    path('bootstrap/<bootstrap>',      Ver1.bootstrap,                 name='Ver1_dashboard'),
    path('plugins/<plugin>',           Ver1.plugins,         name='Ver1_dashboard'),
    path('widget',                     Ver1.widget,         name='Ver1_dashboard'),
    path('form/<form>',                Ver1.form,         name='Ver1_dashboard'),
    path('table/<table>',              Ver1.table,         name='Ver1_dashboard'),
    path('page/<pageData>',            Ver1.page,         name='Ver1_dashboard'),
    ]
