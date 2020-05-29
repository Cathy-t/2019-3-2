#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/5/10 14:05
# @Author  : Cathy 
# @FileName: service.py

import logging
import os
import json
import random
from django.http import JsonResponse

from authorization.models import MoviesList
from backend import settings
from utils.auth import already_authorized, get_user
from utils.response import CommonResponseMixin, ReturnCode
import thirdparty.juhe
from django.core.cache import cache
from utils import timeutil

logger = logging.getLogger('django')


all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
popular_stocks = [
    {
        'code': '000001',
        'name': '平安银行',
        'market': 'sz'
    },
    {
        'code': '000002',
        'name': '万科A',
        'market': 'sz'
    },
    {
        'code': '600036',
        'name': '招商银行',
        'market': 'sh'
    },
    {
        'code': '601398',
        'name': '工商银行',
        'market': 'sh'
    }
]

all_jokes = []


# 股票
def stock(request):
    data = []
    stocks = []
    if already_authorized(request):
        user = get_user(request)
        stocks = json.loads(user.focus_stocks)
    else:
        stocks = popular_stocks
    for stock in stocks:
        result = thirdparty.juhe.stock(stock['market'], stock['code'])
        data.append(result)
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
    pass


#  星座运势
def constellation(request):
    data = []
    if already_authorized(request):
        user = get_user(request)
        constellations = json.loads(user.focus_constellations)
    else:
        constellations = all_constellations

    for c in constellations:
        result = cache.get(c)
        if not result:
            result = thirdparty.juhe.constellation(c)
            timeout = timeutil.get_day_left_in_second()
            cache.set(c, result, timeout)
            logger.info('set cache. key = [%s], value = [%s], timeout = [%d]' % (
                c, result, timeout
            ))
        data.append(result)
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
    pass


def joke(request):
    global all_jokes
    if not all_jokes:
        all_jokes = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r'))
    limits = 10
    sample_jokes = random.sample(all_jokes, limits)
    response = CommonResponseMixin.wrap_json_response(data=sample_jokes)
    return JsonResponse(data=response, safe=False)


def movies(request):
    data = []

    if already_authorized(request):

        #取出可能会感兴趣的movies
        user = get_user(request)
        movie = user.focus_movies

        movie_list = movie.split(',')

    for m in movie_list:
        #通过itemid查询movies表中的id
        movie_names = MoviesList.objects.getId(id=m)
        data.append(movie_names)

    response = CommonResponseMixin.wrap_json_response(data=data)
    return JsonResponse(data=response, safe=False)









