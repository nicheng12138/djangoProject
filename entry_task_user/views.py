# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import socket

from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth

import conf.conf
from conf.log import log
from entry_task_user.common.schema import LoginSchema, UpdateUserSchema
from entry_task_user.common.verify_util import parse_params, verify_token
from entry_task_user.manager import login_manager, user_manager
from rpc.rpc_client import rpc_client
from tcpServer.common.var import Code


def health(request):
    log.info("url = /health: ip=%s" % (request.META.get('REMOTE_ADDR')))
    return JsonResponse({"health": "success"})


def index(request):
    return render(request, "templates/login.html")

@parse_params(form=LoginSchema)
def login(request, data):
    log.info("url = /login, data=%s", data)
    username = data['username']
    pwd = data['password']
    code, data = login_manager.login(username, pwd)
    if code != Code.SUC:
        return render(request, 'templates/login.html', data)
    response = render(request, 'templates/user.html', data)
    response.set_cookie('token', data['token'])
    response.set_cookie('uid', data['uid'])
    return


@csrf_exempt
@verify_token()
@parse_params(form=UpdateUserSchema)
def update_user(request):
    data = json.loads(request.body)
    nickname = data['nickname']
    id = request.COOKIES.get("uid")
    picture = data['picture']
    code, result = user_manager.update_user(id, nickname, picture)
    return JsonResponse(result)



@verify_token()
def get_token(request):
    access_key = "8J_W4UfqsRPWQ5K4X0nb5lxrvcqJGOOkLLwB3gmF"
    secret_key = "V20AyRsE8R94ahRgPjZq7mBv5o8ofkBOBqMu676d"
    q = Auth(access_key, secret_key)
    bucket_name = 'entry_task_user'
    token = q.upload_token(bucket_name)
    return JsonResponse({'uptoken': token})


@csrf_exempt
@verify_token()
def logout(request):
    token = request.COOKIES.get("token")
    code, result = login_manager.logout(token)
    response = JsonResponse(result)
    response.delete_cookie('token')
    response.delete_cookie('uid')
    return response


@verify_token()
def get_user(request):
    uid = request.COOKIES.get("uid")
    code, result = login_manager.logout(token)
