#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : imooc
# @Email          : imooc@foxmail.com
# @Created at     : 2018/12/25
# @Filename       : init.py
# @Desc           :


import os
import json
import yaml
import django
import hashlib
import logging

from backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apis.models import App


def init_app_data():
    old_apps = App.objects.all()
    path = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        apps = yaml.load(f)
        published = apps.get('published')
        for item in published:
            item = item.get('app')
            # 生成唯一id
            src = item.get('category') + item.get('application')
            appid = hashlib.md5(src.encode('utf8')).hexdigest()
            # 存在更新 不存在新建
            if len(old_apps.filter(appid=appid)) == 1:
                print('already exist, appid:', appid)
                app = old_apps.filter(appid=appid)[0]
            else:
                app = App()
                print('not exist, appid:', appid)
            app.appid = appid
            app.name = item.get('name')
            app.application = item.get('application')
            app.url = item.get('url')
            app.publish_date = item.get('publish_date')
            app.category = item.get('category')
            app.desc = item.get('desc')
            app.save()


if __name__ == '__main__':
    init_app_data()