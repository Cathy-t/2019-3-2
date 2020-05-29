import json

from django.http import HttpResponse,JsonResponse, FileResponse

# 调用封装好的API
from authorization.models import User
from thirdparty import juhe

from django.views import View
from utils.response import CommonResponseMixin, ReturnCode

import utils

def helloworld(request):
    print('request method: ', request.method)
    print('request META: ', request.META)
    print('request cookies: ', request.COOKIES)
    print('request QueryDict: ',request.GET)

    # content 表示应答内容；status 表示状态码
    # return HttpResponse(content='Hello Django Response', status=201)

    m = {
        "message": "Hello Django Response"
    }
    # data 表示内容 ； safe=False 即不检查任何的json对象，会默认的把任何的python对象都转化为json；若为true，则只能转化python的字典对象
    return JsonResponse(data=m, safe=False, status=200)
    pass


class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        if not utils.auth.already_authorized(request):
            response = self.wrap_json_response({ }, code=ReturnCode.UNAUTHORIZED)

        else:
            data = []
            open_id = request.session.get('open_id')
            user = User.objects.filter(open_id=open_id)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = juhe.weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)

        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):

        data = []

        received_body = request.body.decode('utf-8')
        # 利用json进行解码
        received_body = json.loads(received_body)

        # 从json中获取城市,使用post的话可以使用一个列表
        cities = received_body.get('cities')
        for city in cities:
            result = juhe.weather(city.get('city'))
            result['city_info'] = city
            data.append(result)

        data = self.wrap_json_response(data=data)
        return JsonResponse(data=data, safe=False)

        pass
