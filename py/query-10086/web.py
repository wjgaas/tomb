#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import os
import httplib
import pickle
import os
import re
import string
import socket
import urlparse
import traceback
import random
import sqlite3

pid = os.getpid()
socket.setdefaulttimeout(10)
conn = sqlite3.connect('input.db')

class CookieManager:
    def __init__(self, pid):
        self.path = './att/pid-%d.cookies' % (pid)
        self.cookies = {}

    def load(self):
        if not os.path.exists(self.path): return {}
        f = open(self.path)
        self.cookies = pickle.load(f)
        f.close()
        print 'Cookies loaded:'
        print self.cookies
        return self.cookies

    def store(self):
        f = open(self.path, 'w')
        pickle.dump(self.cookies, f)
        f.close()

    def update(self, v):
        if not v: return
        ss = v.split(', ')
        for s in ss:
            s = s.split(';')[0].strip()
            try:
                (sk, sv) = s.split('=')
                print '# set-cookie: %s = %s'%(sk, sv)
                self.cookies[sk] = sv
            except Exception as e:
                pass
        self.store()

    def to_string(self):
        return string.join(map(lambda k : '%s=%s'%(k, self.cookies[k]), self.cookies), '; ')

def vcode_file(id):
    return 'att/vcode-%d.jpg'%(id)

def default_headers():
    headers = {}
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'
    # we don't want to handle gzip.
    # headers['Accept-Encoding'] = 'gzip,deflate'
    headers['Accept-Language'] = 'en-US,en;q=0.8,zh-CN;q=0.6'
    return headers

def randomly_select_phone():
    c = conn.cursor()
    c.execute('SELECT phone FROM pb WHERE marked = 0 LIMIT 10')
    ps = c.fetchall()
    if len(ps) == 0: return None
    idx = random.randint(0, len(ps) - 1)
    p = str(ps[idx][0])
    return p

def update_phone_balance(phone, balance):
    c = conn.cursor()
    c.execute('UPDATE pb SET balance = ?, marked = 1 WHERE phone = ?', (balance, phone,))
    conn.commit()

def step1(cm, headers):
    print '-----step1-----'
    host = 'zj.ac.10086.cn'
    headers['Host'] = host
    headers['Cookie'] = cm.to_string()
    conn = httplib.HTTPSConnection(host)
    req = conn.request('GET', '/login', '', headers)
    res = conn.getresponse()
    cm.update(res.getheader('set-cookie'))
    res.read() # discard it.o

    req = conn.request('GET', '/ImgDisp', '', headers)
    res = conn.getresponse()
    vcode = vcode_file(pid)
    open(vcode, 'w').write(res.read())
    conn.close()

def step2(cm, headers, phone, code):
    print '-----step2-----'
    host = 'zj.ac.10086.cn'
    headers['Host'] = host
    headers['Content-Length'] = '263'
    headers['Cache-Control'] = 'max-age=0'
    headers['Origin'] = 'https://zj.ac.10086.cn'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Referer'] =  'https://zj.ac.10086.cn/login'
    headers['Cookie'] = cm.to_string()
    body = 'service=my&continue=%2Fmy%2Flogin%2FloginSuccess.do&failurl=https%3A%2F%2Fzj.ac.10086.cn%2Flogin&style=1&pwdType=2&SMSpwdType=0&billId=' + phone + '&passwd1=%CD%FC%BC%C7%C3%DC%C2%EB%A3%BF%BF%C9%D3%C3%B6%AF%CC%AC%C3%DC%C2%EB%B5%C7%C2%BC&passwd=150792&validCode=' + code

    conn = httplib.HTTPSConnection(host)
    req = conn.request('POST', '/loginbox', body, headers)
    res = conn.getresponse()
    if res.status != 200: return
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r'name="SAMLart" value="([\w\d]+)"', page)
    SAMLart = m.groups()[0]
    print 'SAMLart =', SAMLart
    return SAMLart

def step3(cm, headers, SAMLart):
    print '-----step3-----'
    host = 'www.zj.10086.cn'
    headers['Host'] = host
    headers['Content-Length'] = '97'
    headers['Cookie'] = cm.to_string()
    body = 'SAMLart=' + SAMLart + '&RelayState=%2Fmy%2Flogin%2FloginSuccess.do&submit=Submit'

    conn = httplib.HTTPConnection(host)
    req = conn.request('POST', '/my/sso', body, headers)
    res = conn.getresponse()
    if res.status != 200 and res.status != 302: return
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r"name='SAMLart' value='([\w\d]+)'", page)
    SAMLart = m.groups()[0]
    print 'SAMLart =', SAMLart
    return SAMLart

def step4(cm, headers, SAMLart):
    print '-----step4-----'
    host = 'www.zj.10086.cn'
    headers['Content-Length'] = '224'
    headers['Origin'] = 'http://www.zj.10086.cn'
    headers['Referer'] = 'http://www.zj.10086.cn/my/sso'
    headers['Cookie'] = cm.to_string()
    body = 'RelayState=%252Fmy%252Flogin%252FloginSuccess.do&SAMLart=' + SAMLart + '&jumpUrl=%252Fmy%252Flogin%252FloginSuccess.do&loginUrl=http%253A%252F%252Fwww.zj.10086.cn%252Fmy%252Flogin%252Flogin.jsp&submit=Submit'

    conn = httplib.HTTPConnection(host)
    req = conn.request('POST','/my/UnifiedLoginClientServlet', body, headers)
    res = conn.getresponse()
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()

def step5(cm, headers):
    print '-----step5-----'
    host = 'www.zj.10086.cn'
    del headers['Content-Length']
    del headers['Content-Type']
    del headers['Origin']
    del headers['Referer']
    headers['Cookie'] = cm.to_string()

    conn = httplib.HTTPConnection(host)
    req = conn.request('GET','/my/login/loginSuccess.do', headers = headers)
    res = conn.getresponse()
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()

def step7(cm, headers):
    print '-----step7-----'
    host = 'www.zj.10086.cn'
    headers['Host'] = host
    headers['Cookie'] = cm.to_string()
    conn = httplib.HTTPConnection(host)
    req = conn.request('GET','/my/include/mybill.jsp', headers = headers)
    res = conn.getresponse()
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r'http://service.zj.10086.cn/yw/bill/billDetail.do\?bid=([\w\d]+)&month=0', page)
    url = '/yw/bill/billDetail.do?bid=%s&month=0'%(m.groups()[0])
    return url

def step8(cm, headers, url):
    print '-----step8-----'
    conn = httplib.HTTPConnection('service.zj.10086.cn')
    headers['Host'] = 'service.zj.10086.cn'
    headers['Cookie'] = cm.to_string()
    req = conn.request('GET',url, headers = headers)
    res = conn.getresponse()
    cm.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    def to_gb2312(s): return s.decode('utf-8').encode('gb2312')
    def to_utf8(s): return s.decode('gb2312').encode('utf-8')
    rex1 = r'<b>%s</b></th><td width="\d+" align="left" class="money">([\S]+) '%(to_gb2312('充值账户实际可用余额/充值账户余额'))
    m1 = re.search(rex1, page)
    rex2 = r'<tr><th><strong>%s</strong>%s</th><td>([^<]+)</td></tr><tr><th><strong>%s</strong>%s</th><td>(\d+)</td></tr' % (to_gb2312('客　　户'),
                                                                                                                             to_gb2312('：'),
                                                                                                                             to_gb2312('号　　码'),
                                                                                                                             to_gb2312('：'))
    m2 = re.search(rex2, page)
    (balance, company, number) = (m1.groups()[0], to_utf8(m2.groups()[0]), m2.groups()[1])
    return (balance, company, number)

def process(env, start_response):
    global pid
    path = env['PATH_INFO']
    qs = env['QUERY_STRING']
    home_ok = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><meta http-equiv="refresh" content="2; url=/"/></head><body><p>成功更新，2秒后跳回主页面</p></html>"""
    home_f1 = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><meta http-equiv="refresh" content="2; url=/"/></head><body><p>出现未知异常，2秒后跳回主页面</p></body></html>"""
    home_f2 = """<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body><p>出现如下异常</p><pre>%s</pre></body></html>"""

    if path == '/':
        phone = randomly_select_phone()
        if not phone:
            start_response('200 OK', [('Content-Type','text/html')])
            return ('<html><body><p>ALL DONE!!!</p></body></html>',)

        cm = CookieManager(pid)
        cm.load()
        headers = default_headers()
        try:
            step1(cm, headers)
            start_response('200 OK', [('Content-Type','text/html')])
            kvs = {'vcode': vcode_file(pid),
                    'id': pid,
                    'phone': phone}
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
        headers = default_headers()

        def cont():
            SAMLart = step2(cm, headers, phone, code)
            if not SAMLart: return
            SAMLart = step3(cm, headers, SAMLart)
            if not SAMLart: return
            step4(cm, headers, SAMLart)
            step5(cm, headers)
            url = step7(cm, headers)
            return step8(cm, headers, url)

        try:
            res = cont()
            if res:
                print '-----update %s OK-----'%(phone)
                (balance, company, number) = res
                update_phone_balance(phone, float(balance))
                start_response('200 OK',[('Content-Type','text/html')])
                return (home_ok,)
            else:
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

from wsgiref.validate import validator
from wsgiref.simple_server import make_server
def main():
    vrun=validator(run)
    httpd = make_server('', 8000, vrun)
    httpd.serve_forever()

main()
