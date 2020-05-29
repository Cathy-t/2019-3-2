#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         : imooc
# @Email          : imooc@foxmail.com
# @Created at     : 2018/11/30
# @Filename       : image.py
# @Desc           :
import hashlib
import os
import utils.response
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.views import View

from backend import settings

from utils.response import ReturnCode, CommonResponseMixin


class ImageListView(View, CommonResponseMixin):
    def get(self, request):
        image_files = os.listdir(settings.IMAGES_DIR)
        response_data = []

        # 返回每个图片的名字和md5
        for image_file in image_files:
            response_data.append({
                "name": image_file,
                "md5": image_file[:-4]
            })
        response_data = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response_data)

    pass


# 定义一个类视图，来优化处理逻辑
class ImageView(View, utils.response.CommonResponseMixin):
    def get(self,request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        print(imgfile)
        if os.path.exists(imgfile):
            data = open(imgfile,'rb').read()

            # return HttpResponse(content=data, content_type='image/jpeg')
            # 利用fileresponse来返回图片消息
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpeg')

        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)


    def post(self,request):
        """
        上传文件，获取文件信息,此时的文件存储形式是<key,value>形式
        key：为文件上传的名字；value:为文件的二进制存储形式(内容)
        """
        files = request.FILES
        response = []

        for key, value in files.items():
            content = value.read()
            # 将md5以十六进制保存
            md5 = hashlib.md5(content).hexdigest()

            # 保存文件
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            with open(path, 'wb') as f:
                f.write(content)

            response.append({
                'name': key,
                'md5': md5
            })

        message = 'post message success .'
        # response = utils.response.wrap_json_response(message=message)

        # 使用Mixin的模式
        response = self.wrap_json_response(data=response, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response, safe=False)
        pass

    def put(self,request):
        message = 'put message success .'
        # response = utils.response.wrap_json_response(message=message)

        # 使用Mixin的模式
        response = self.wrap_json_response(message=message)
        return JsonResponse(data=response, safe=False)
        pass

    def delete(self, request):
        """
        对本地的文件进行删除
        """

        # 表示从请求的请求参数中取出md5
        md5 = request.GET.get('md5')
        img_name = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, img_name)

        if os.path.exists(path):
            os.remove(path)
            message = 'remove success .'
        else:
            message = 'file(%s) not found .' % img_name
        # response = utils.response.wrap_json_response(message=message)

        # 使用Mixin的模式
        response = self.wrap_json_response(message=message)
        return JsonResponse(data=response, safe=False)
        pass


def image_text(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if not os.path.exists(imgfile):

            return utils.response.wrap_json_response(code=ReturnCode.RESOURCES_NOT_EXISTS)

        else:
            response_data = {}
            response_data['name'] = md5 + '.jpg'
            response_data['url'] = '/service/image?md5=%s' % (md5)
            response = utils.response.wrap_json_response(data=response_data)
            return JsonResponse(data = response, safe=False)

