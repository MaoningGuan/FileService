# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'fileOperate'
urlpatterns = [
    path('', views.index, name='index'),
    re_path('download/(?P<filename>.+)', views.download, name='download'),

    # url(r'^upload/$', views.upload, name='upload'),
    # url(r'^download/(?P<filename>.+)$', views.download, name='download'),

]