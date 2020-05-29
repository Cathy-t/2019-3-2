import json

from django.shortcuts import render

from utils.auth import c2s, already_authorized
from .models import User

# Create your views here.

from django.http import JsonResponse
from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin

from django.views import View


def test_session(request):
    request.session['message'] = 'Test Django Session OK!'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def test_session2(request):
    print('session content: ', request.session.items())
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


class UserView(View, CommonResponseMixin):
    # 关注的城市、股票和星座

    # get方法为获取用户的数据
    def get(self, request):
        # 判断用户是否已经登录
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)

        # 若已经登录则获取openid
        open_id = request.session.get('open_id')
        # 获取到open_id后可以从数据库中获取到用户
        user = User.objects.get(open_id=open_id)
        # 找到用户后，将用户关注的信息进行返回
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        data['focus']['stock'] = json.loads(user.focus_stocks)

        # 对查询到的结果进行返回
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

        pass

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)

        # 对用户的信息进行修改
        # 取出request信息，并进行转换,将其变成字典
        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        # 从转换的字典中取出星座、股票等,并放入user这个对象中
        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')

        user.focus_cities = json.dumps(cities)
        user.focus_stocks = json.dumps(stocks)
        user.focus_constellations = json.dumps(constellations)
        user.save()

        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message='modify user info success .')
        return JsonResponse(data=response, safe=False)
        pass


def __authorize_by_code(request):
    """
    使用wx.login的到的临时code到微信提供的code2session接口授权
    """

    post_data = request.body
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()

    response = {}
    if not code or not app_id:
        response['message'] = 'authorized failed, need entire authorization data.'
        response['code '] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)

    data = c2s(app_id, code)
    openid = data.get('openid')
    print('get openid: ', openid)
    if not openid:
        response = wrap_json_response(code=ReturnCode.FAILED, message='auth failed')
        return JsonResponse(data=response, safe=False)

    # 标记这个openid的用户已经在线
    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    # 判断用户是否在数据库中
    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid, nickname=nickname)
        print('new user: open_id: %s, nickname: %s' % (openid, nickname))
        new_user.save()

    response = wrap_json_response(code=ReturnCode.SUCCESS, message='auth success.')
    return JsonResponse(data=response, safe=False)
    pass


def authorize(request):
    return __authorize_by_code(request)


def logout(request):
    """
    实现注销功能
    """
    request.session.clear()
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
    pass


# 判断是否已经登陆
def get_status(request):
    print('call get_status function...')
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)