# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth

from rpc.rpcClient import RPCClient


def index(request):
    return render(request, "templates/login.html")


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    client = RPCClient()
    client.connect('127.0.0.1', 5000)
    result = client.login(username, password)
    data = eval(result)
    print data['code']
    if data['code'] == -1 or data['code'] == -2:
        return render(request, "templates/login.html", data)

    return render(request, "templates/user.html", data)


def user(request):
    context = {
        'username': 'dhasiu',
        'nickname': 'csd',
        'picture': 'r47q6lm7l.hn-bkt.clouddn.com/1639712643915'
    }
    return render(request, "templates/user.html", context)


@csrf_exempt
def update_user(request):
    print request.POST.get('nickname')
    print request.POST.get('picture')
    return JsonResponse({'msg': 'success'})


def get_token(request):
    access_key = "8J_W4UfqsRPWQ5K4X0nb5lxrvcqJGOOkLLwB3gmF"
    secret_key = "V20AyRsE8R94ahRgPjZq7mBv5o8ofkBOBqMu676d"
    q = Auth(access_key, secret_key)
    bucket_name = 'entrytask'
    token = q.upload_token(bucket_name)
    return JsonResponse({'uptoken': token})


@csrf_exempt
def logout(request):
    response = JsonResponse({})
    response.delete_cookie('login')
    return response
