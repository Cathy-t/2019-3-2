# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 20:34
# @Author  : Cathy
# @FileName: version_1_0.py
# @Software: PyCharm

from django.urls import path, include

urlpatterns = [
    path('service/', include('apis.urls')),
    path('auth/', include('authorization.urls'))
]