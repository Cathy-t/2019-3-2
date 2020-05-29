# -*- encoding=utf8 -*-

from django.db import models

# Create your models here.
from apis.models import App


class User(models.Model):
    # open_id 即为一个长度为32的字符串
    open_id = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=256)

    # 关注的城市
    focus_cities = models.TextField(default='[]')
    # 关注的星座
    focus_constellations = models.TextField(default='[]')
    # 关注的股票
    focus_stocks = models.TextField(default='[]')
    # 可能会关注的电影
    focus_movies = models.TextField(default='[]')

    # 创建用户与应用的多对多映射
    menu = models.ManyToManyField(App)

    def __str__(self):
        return '%s' % (self.nickname)


class MoviesList(models.Model):
    movie_title = models.TextField(default='')
    movie_genres = models.TextField(default='')

