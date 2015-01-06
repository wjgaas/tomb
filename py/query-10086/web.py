#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from common import *
import os
import traceback
import urlparse

pid = os.getpid()
cp = ConnectionPool()
pb = PhoneBalanceDB('input.db')

headers = cp.default_headers()
try:
    cm = CookieManager(pid)
    vcode = VCode(pid)
    print '-----初始化cookie-----'
    initial_cookie(cm, cp, vcode, headers)
except Exception as e:
    print '-----初始化cookie发生异常-----'
    traceback.print_exc()
    pass

def process(env, start_response):
    global pid, cp, pb

    path = env['PATH_INFO']
    qs = env['QUERY_STRING']

    home_ok = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><meta http-equiv="refresh" content="2; url=/"/></head><body><p>更新成功，2秒后跳回主页面</p></html>"""
    home_f1 = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><meta http-equiv="refresh" content="2; url=/"/></head><body><p>更新失败，2秒后跳回主页面</p></body></html>"""
    home_f2 = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body><p>出现如下异常</p><pre>%s</pre></body></html>"""

    if path == '/':
        phone = pb.randomly_select_phone()
        if not phone:
            start_response('200 OK', [('Content-Type','text/html')])
            return ('<html><body><p>ALL DONE!!!</p></body></html>',)
        cm = CookieManager(pid)
        cm.load()
        vcode = VCode(pid)
        headers = cp.default_headers()
        try:
            initial_cookie(cm, cp, vcode, headers)
            start_response('200 OK', [('Content-Type','text/html')])
            kvs = {'vcode': vcode.path, 'id': pid, 'phone':phone}
            html ="""
<html><body><img src="%(vcode)s"/>
<form action="/cont" method="GET">
<p>Code: <input type="text" name="code" autofocus/></p>
<input type="hidden" name="id" value="%(id)d"/>
<input type="hidden" name="phone" value="%(phone)s"/>
<input type="submit" value="Next"/>
</form>
</body></html>""" % kvs
            return (html,)
        except Exception as e:
            bt = traceback.format_exc()
            start_response('200 OK', [('Content-Type','text/html')])
            return (home_f2 % bt,)

    elif path == '/cont':
        d = urlparse.parse_qs(qs)
        code = d['code'][0]
        vid = int(d['id'][0])
        phone = d['phone'][0]
        cm = CookieManager(vid)
        cm.load()
        headers = cp.default_headers()
        try:
            res = get_phone_balance(cm, cp, headers, phone, code)
            if res:
                (balance, company, number) = res
                pb.update_phone_balance(phone, float(balance))
                print "更新号码 '%s' = %s 成功" % (phone, balance)
                start_response('200 OK',[('Content-Type','text/html')])
                return (home_ok,)
            else:
                print "更新号码 '%s' 失败" % (phone)
                start_response('200 OK',[('Content-Type','text/html')])
                return (home_f1,)
        except Exception as e:
            bt = traceback.format_exc()
            start_response('200 OK',[('Content-Type','text/html')])
            return (home_f2 % bt,)

    else: # others as jpeg files.
        fname = path[1:]
        if os.path.exists(fname):
            start_response('200 OK',
                            [('Content-Type','applicaiton/jpeg')])
            data = open(fname).read()
            return (data,)
        else:
            start_response('400 Not Found', [('Content-Type','text/html')])
            return ('',)

def run(env, start_response):
    try:
        return process(env, start_response)
    except Exception as e:
        print e
        start_response('500 Error', [('Content-Type','text/html')])
        return ('Internal Server Error',)

if __name__ == '__main__':
    from wsgiref.validate import validator
    from wsgiref.simple_server import make_server
    vrun=validator(run)
    httpd = make_server('', 8000, vrun)
    httpd.serve_forever()
