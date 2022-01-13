# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps

from django.db import models

# Create your models here.
from django.shortcuts import render

from conf import conf
from conf.log import log

from rpc.rpc_client_pool import rpc_client_pool


client_pool = rpc_client_pool(conf.RPC_SVR_IP, conf.RPC_SVR_PORT)


def req_rpc(func, *args, **kwargs):
    client = client_pool.get_rpc_client()
    try:
        result = client.call(func, args, kwargs)
    except Exception as e:
        log.info("socket error:error_type = %s |func = %s|args= %s|kwargs = %s" % (e, func, str(args), str(kwargs)))
        return None
    finally:
        client_pool.release_rpc_client(client)
    return result

def verify_token():
    def _verify_token(func):
        @wraps(func)
        def _func(request, *args, **kwargs):
            token = request.COOKIES.get('token')
            uid = request.COOKIES.get('uid')
            is_valid = req_rpc('check_token', (token, uid))
            if not is_valid:
                data = {
                    'msg': "token is expire or is valid"
                }
                return render(request, 'templates/login.html', data)
            func(request, args, kwargs)
        return _func
    return _verify_token

