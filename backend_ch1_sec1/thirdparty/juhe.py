#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : cathy
# @Email          : imooc@foxmail.com
# @Created at     : 2019/04/14
# @Filename       : juhe.py


import json
import requests

from utils import proxy


def weather(cityname):
    """
    :param cityname: 城市名字
    :return: 返回实况天气
    """
    key = 'ea23ad30f47f85f1cf2c7982c2ef2638'
    api = 'http://v.juhe.cn/weather/index'
    params = 'cityname=%s&key=%s' % (cityname, key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    json_data = json.loads(response.text)
    print(json_data)
    result = json_data.get('result')
    sk = result.get('sk')
    response = dict()
    response['temperature'] = sk.get('temp')
    response['wind_direction'] = sk.get('wind_direction')
    response['wind_strength'] = sk.get('wind_strength')
    response['humidity'] = sk.get('humidity')  # 湿度
    response['time'] = sk.get('time')
    return response


def stock(market, code):
    """
    沪深股票
    :param market: 上交所 = sh, 深交所 = sz
    :param code: 股票编号
    :return:
    """
    key = 'bbe128988ed5d8042671d900248fa8ca'
    api = 'http://web.juhe.cn:8080/finance/stock/hs'
    params = 'gid=%s&key=%s' % (market + code, key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    data = data.get('result')[0].get('data')
    response = {'name': data.get('name'),
                'now_price': data.get('nowPri'),
                'today_min': data.get('todayMin'),
                'today_max': data.get('todayMax'),
                'start_price': data.get('todayStartPri'),
                'date': data.get('date'),
                'time': data.get('time')
                }
    response['is_rising'] = data.get('nowPri') > data.get('todayStartPri')
    sub = abs(float(data.get('nowPri')) - float(data.get('todayStartPri')))  # 差值
    response['sub'] = float('%.3f' % sub)
    return response


def constellation(cons_name):
    '''
    :param cons_name: 星座名字
    :return: json 今天运势
    '''
    key = 'be7fc7af90fee30cdfa042353cc2ce15'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    types = ('today', 'tomorrow', 'week', 'month', 'year')
    params = 'consName=%s&type=%s&key=%s' % (cons_name, types[0], key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    return {
        'name': cons_name,
        'text': data['summary']
    }


if __name__ == '__main__':
    data = weather('武汉')
