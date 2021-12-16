# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from Carbon.Fonts import mobile
from os import path

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from djangoProject import settings


def index(request):
    return render(request, "templates/login.html")


@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print username + ',' + password
    data = {
        'code': 200,
        'msg': "登陆成功"
    }
    if data['code'] == 200:
        return redirect('/user', data)
    return JsonResponse({'code': 200, 'msg': "登陆成功"}, charset='utf-8', json_dumps_params={'ensure_ascii': False})


def user(request):
    context = {
        'username': 'dhasiu',
        'nickname': 'dasda',
        'picture': '1.jpeg'
    }
    return render(request, "templates/user.html", context)


def files(request):
    # 获取 上传的 图片信息
    img = request.FILES.get('avatar')
    # 获取上传图片的名称
    img_name = img.name
    suf = img_name.split('.')[1]
    if suf != 'png' and suf != 'jpg' and suf != 'jpeg':
        context = {'msg': '文件格式错误，请上传图片！'}
        return render(request, "templates/user.html", context)
    # 图片保存路径
    img_path = os.path.join(settings.IMG_UPLOAD, img_name)
    print img_path
    # 写入 上传图片的 内容
    with open(img_path, 'ab') as fp:
        # 如果上传的图片非常大， 那么通过 img对象的 chunks() 方法 分割成多个片段来上传
        for chunk in img.chunks():
            fp.write(chunk)

    return HttpResponse('uploads success')


def my_image(request):
    picture = request.GET.get('picture')
    image_path = os.path.join(settings.IMG_UPLOAD + '/' + picture)
    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
