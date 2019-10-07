from __future__ import  absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置celery的环境变量和django-celery的工作目录
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CeleryTask.settings')

# 实例化celery应用
app=Celery("art_project")  #celery服务器的名称
app.config_from_object('django.conf:settings')  #：加载celery的配置
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)
#如果在项目当中，创建了task.py,那么celery就会沿着app去查找task.py来生成任务



