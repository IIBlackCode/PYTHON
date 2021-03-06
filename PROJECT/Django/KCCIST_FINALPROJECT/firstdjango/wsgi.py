"""
wsgi.py 역할

배포 관련 설정
웹사이트 실행 프로세스 관련 설정

WSGI config for firstdjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstdjango.settings')

application = get_wsgi_application()
