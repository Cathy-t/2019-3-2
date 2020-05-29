#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : imooc
# @Email          : imooc@foxmail.com
# @Created at     : 2018/12/20
# @Filename       : urls.py
# @Desc           :


from django.urls import path

from authorization import views

urlpatterns = [
    path('test', views.test_session),
    # path('test2', views.test_session2),

    path('authorize', views.authorize, name='authorize'),
    path('user', views.UserView.as_view()),
    path('logout', views.logout, name='logout'),
    path('status', views.get_status, name='get_status')
]