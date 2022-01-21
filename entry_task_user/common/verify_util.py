import json
from functools import wraps

import jsonschema as jsonschema
from django.http import JsonResponse
from django.shortcuts import render

from conf.log import log
from entry_task_user.manager.rpc_manager import req_rpc


def verify_token():
    def _verify_token(func):
        @wraps(func)
        def _func(request, *args, **kwargs):
            token = request.COOKIES.get('token')
            uid = request.COOKIES.get('uid')
            is_valid = req_rpc('check_token', (token, uid))
            if not is_valid:
                log.info("error token|token = %s, uid = %s" % (token, uid))
                data = {
                    'msg': "token is expire or is valid"
                }
                return render(request, 'templates/login.html', data)
            func(request, *args, **kwargs)
        return _func
    return _verify_token


def parse_params(form):
    form = jsonschema.Draft4Validator(form)
    def _parse_params(func, *args, **kwargs):
        @wraps(func)
        def _func(request, ):
            try:
                data = json.loads(request.body)
                form.validate(data)
            except jsonschema.ValidationError as ex:
                data = {
                    'msg': "error params"
                }
                log.info("vail params fail|data = %s" % data)
                return JsonResponse(data)
            except Exception as e:
                data = {
                    'msg': "error params"
                }
                log.info("load json fail|error_msg =%s| request.body = %s" % (e, request.body))
                return JsonResponse(data)
            func(request, data, *args, **kwargs)
        return _func
    return _parse_params
