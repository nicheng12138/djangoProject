# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import socket

from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth

import conf.conf
from rpc.rpcClient import RPCClient
from tcpServer.var import Code



def index(request):
    return render(request, "templates/login.html")


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        return render(request, "templates/login.html")
    client = RPCClient()
    client.connect(conf.conf.RPC_SVR_IP, conf.conf.RPC_SVR_PORT)
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
    try:
        data = json.loads(request.body)
        token = data['token']
        nickname = data['nickname']
        username = data['username']
        picture = data['picture']
        client = RPCClient()
        client.connect(conf.conf.RPC_SVR_IP, conf.conf.RPC_SVR_PORT)
        result = client.update_user(token, nickname, picture, username)
        client.close()
        if result is None:
            return JsonResponse({"code": Code.FAIL, "msg": "fail"})
        elif result['code'] == Code.AUTH_FAIL:
            return JsonResponse(result)
        elif result['code'] == Code.TOKEN_INVALID:
            return JsonResponse(result)
        return JsonResponse(result)
    except IOError as e:
        return JsonResponse({"code": Code.FAIL, "msg": "fail"})
    except Exception as e:
        return JsonResponse({"code": Code.FAIL, "msg": "fail"})


def get_token(request):
    access_key = "8J_W4UfqsRPWQ5K4X0nb5lxrvcqJGOOkLLwB3gmF"
    secret_key = "V20AyRsE8R94ahRgPjZq7mBv5o8ofkBOBqMu676d"
    q = Auth(access_key, secret_key)
    bucket_name = 'entry_task_user'
    token = q.upload_token(bucket_name)
    return JsonResponse({'uptoken': token})


@csrf_exempt
def logout(request):
    token = request.POST.get('token')
    client = RPCClient()
    client.connect(conf.conf.RPC_SVR_IP, conf.conf.RPC_SVR_PORT)
    res = client.logout(token)
    client.close()
    response = JsonResponse(res)
    response.delete_cookie('token')
    return response


def get_user(request):
    token = request.COOKIES.get('token')
    username = None
    if token is None:
        try:
            data = json.loads(request.body)
            username = data['username']
            token = data['token']
        except Exception as e:
            print "Exception:" + str(e)
            return render(request, "templates/login.html", {
                'msg': 'token is invalid'
            })
    try:
        client = RPCClient()
        client.connect(conf.conf.RPC_SVR_IP, conf.conf.RPC_SVR_PORT)
        result = client.get_user(token, username)
        client.close()
        if token == 'tokenTest':
            return JsonResponse(result)
        if result['code'] != 0:
            return render(request, "templates/login.html", result)
        res = result['data']
        data = {
            'username': res['username'],
            'nickname': res['nickname'],
            'picture': res['picture']
        }
        return render(request, 'templates/user.html', data)
    except socket.error as e:
        return JsonResponse({"code": Code.FAIL, "msg": "fail", "data": None})
