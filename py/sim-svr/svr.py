#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from flask import Flask
from flask import make_response
from flask import request

app = Flask(__name__)
app.debug = True

from common2 import *
p = Process()

import traceback
import json

def retry(func, args, cond, count = 3):
    res = None
    while count > 0:
        try:
            (ok, retval) = apply(func, args)
        except Exception as e:
            # 发生异常
            app.logger.warning(traceback.format_exc())
            count -= 1
            continue
        res = (ok, retval)
        if not cond(ok, retval): # 不满足条件
            count -= 1
            continue
        else: break
    return res

def make_resp(js, cb):
    s = json.dumps(js)
    if cb:
        s = cb + '(%s)' % s
        resp = make_response(s)
        resp.headers['Content-Type'] = 'application/javascript'
    else:
        resp = make_response(s)
        resp.headers['Content-Type'] = 'text/json'
    return resp

@app.route('/init', methods = ['GET'])
def init():
    phone = request.args.get('phone').decode('utf-8')
    cb = request.args.get('cb', '').decode('utf-8')
    res = retry(p.above_half, (phone,), lambda ok, res: True)
    if not res:
        # 查询验证码失败
        js = {'code': 1, 'msg':'get captcha faild'}
    else:
        (ok, res) = res
        # 已经查询到余额
        if ok: js = {'code':0, 'msg':'bal', 'data': res}
        # 否则返回token
        else: js = {'code':0, 'msg':'token', 'data': res}
    return make_resp(js, cb)

@app.route('/query', methods = ['GET'])
def query():
    token = request.args.get('token').decode('utf-8')
    code = request.args.get('code').decode('utf-8')
    cb = request.args.get('cb', '').decode('utf-8')
    res = retry(p.bottom_half, (token, code), lambda ok, res: ok)
    if not res or not res[0]:
        # 查询余额失败
        js = {'code': 1, 'msg': 'query balance failed'}
    else:
        js = {'code': 0, 'msg': 'bal', 'data': res[1]}
    return make_resp(js, cb)

if __name__ == '__main__':
    app.run()
