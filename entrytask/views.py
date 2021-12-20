# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth

from rpc.config import conf
from rpc.rpcClient import RPCClient
from tcpServer.var import Code


def index(request):
    return render(request, "templates/login.html")


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print password
    if username is None or password is None:
        return render(request, "templates/login.html")
    client = RPCClient()
    client.connect(conf.host, conf.port)
    result = client.login(username, password)
    client.close()
    if result['code'] != 0:
        return render(request, "templates/login.html", result)
    res = result['data']
    data = {
        'username': res['username'],
        'nickname': res['nickname'],
        'picture': res['picture']
    }
    response = render(request, 'templates/user.html', data)
    response.set_cookie('token', res['token'])
    return response


@csrf_exempt
def update_user(request):
    token = request.POST.get('token')
    nickname = request.POST.get('nickname')
    picture = request.POST.get('picture')
    client = RPCClient()
    client.connect(conf.host, conf.port)
    print token
    result = client.update_user(token, nickname, picture)
    client.close()
    if result['code'] == Code.AUTH_FAIL:
        render(request, 'templates/login.html', result)
    return JsonResponse({'msg': result['msg']})


def get_token(request):
    access_key = "8J_W4UfqsRPWQ5K4X0nb5lxrvcqJGOOkLLwB3gmF"
    secret_key = "V20AyRsE8R94ahRgPjZq7mBv5o8ofkBOBqMu676d"
    q = Auth(access_key, secret_key)
    bucket_name = 'entrytask'
    token = q.upload_token(bucket_name)
    return JsonResponse({'uptoken': token})


@csrf_exempt
def logout(request):
    client = RPCClient()
    client.connect(conf.host, conf.port)
    token = request.POST.get('token')
    res = client.logout(token)
    response = JsonResponse(res)
    response.delete_cookie('token')
    return response


def get_user(request):
    token = request.COOKIES.get('token')
    if token is None:
        return render(request, "templates/login.html", {
            'msg': 'token is invalid'
        })
    client = RPCClient()
    client.connect(conf.host, conf.port)
    result = client.get_user(token)
    client.close()
    if result['code'] != 0:
        return render(request, "templates/login.html", result)
    res = result['data']
    data = {
        'username': res['username'],
        'nickname': res['nickname'],
        'picture': res['picture']
    }
    return render(request, 'templates/user.html', data)
