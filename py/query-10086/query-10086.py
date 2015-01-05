#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import httplib
import pickle
import os
import re
import string
import StringIO
from PIL import Image
import socket

class CookieManager:
    def __init__(self):
        self.path = './10086.cookies'
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

cookie_manager = CookieManager()
cookie_manager.load()
socket.setdefaulttimeout(10)

def default_headers():
    headers = {}
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'
    # we don't want to handle gzip.
    # headers['Accept-Encoding'] = 'gzip,deflate'
    headers['Accept-Language'] = 'en-US,en;q=0.8,zh-CN;q=0.6'
    return headers

def step1(headers):
    print '-----step1-----'
    host = 'zj.ac.10086.cn'
    headers['Host'] = host
    headers['Cookie'] = cookie_manager.to_string()
    conn = httplib.HTTPSConnection(host)
    req = conn.request('GET', '/login', '', headers)
    res = conn.getresponse()
    cookie_manager.update(res.getheader('set-cookie'))
    res.read() # discard it.

    req = conn.request('GET', '/ImgDisp', '', headers)
    res = conn.getresponse()
    open('vcode.jfif','w').write(res.read())
    conn.close()
    im = Image.open('vcode.jfif')
    im.show()
    code = raw_input('input code > ').strip()
    return code

def step2(headers, phone, code):
    print '-----step2-----'
    host = 'zj.ac.10086.cn'
    headers['Content-Length'] = '263'
    headers['Cache-Control'] = 'max-age=0'
    headers['Origin'] = 'https://zj.ac.10086.cn'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Referer'] =  'https://zj.ac.10086.cn/login'
    headers['Cookie'] = cookie_manager.to_string()
    body = 'service=my&continue=%2Fmy%2Flogin%2FloginSuccess.do&failurl=https%3A%2F%2Fzj.ac.10086.cn%2Flogin&style=1&pwdType=2&SMSpwdType=0&billId=' + phone + '&passwd1=%CD%FC%BC%C7%C3%DC%C2%EB%A3%BF%BF%C9%D3%C3%B6%AF%CC%AC%C3%DC%C2%EB%B5%C7%C2%BC&passwd=150792&validCode=' + code

    conn = httplib.HTTPSConnection(host)
    req = conn.request('POST', '/loginbox', body, headers)
    res = conn.getresponse()
    if res.status != 200: return
    cookie_manager.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r'name="SAMLart" value="([\w\d]+)"', page)
    SAMLart = m.groups()[0]
    print 'SAMLart =', SAMLart
    return SAMLart

def step3(headers, SAMLart):
    print '-----step3-----'
    host = 'www.zj.10086.cn'
    headers['Host'] = host
    headers['Content-Length'] = '97'
    headers['Cookie'] = cookie_manager.to_string()
    body = 'SAMLart=' + SAMLart + '&RelayState=%2Fmy%2Flogin%2FloginSuccess.do&submit=Submit'

    conn = httplib.HTTPConnection(host)
    req = conn.request('POST', '/my/sso', body, headers)
    res = conn.getresponse()
    if res.status != 200 and res.status != 302: return
    cookie_manager.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r"name='SAMLart' value='([\w\d]+)'", page)
    SAMLart = m.groups()[0]
    print 'SAMLart =', SAMLart
    return SAMLart

def step4(headers, SAMLart):
    print '-----step4-----'
    host = 'www.zj.10086.cn'
    headers['Content-Length'] = '224'
    headers['Origin'] = 'http://www.zj.10086.cn'
    headers['Referer'] = 'http://www.zj.10086.cn/my/sso'
    headers['Cookie'] = cookie_manager.to_string()
    body = 'RelayState=%252Fmy%252Flogin%252FloginSuccess.do&SAMLart=' + SAMLart + '&jumpUrl=%252Fmy%252Flogin%252FloginSuccess.do&loginUrl=http%253A%252F%252Fwww.zj.10086.cn%252Fmy%252Flogin%252Flogin.jsp&submit=Submit'

    conn = httplib.HTTPConnection(host)
    req = conn.request('POST','/my/UnifiedLoginClientServlet', body, headers)
    res = conn.getresponse()
    cookie_manager.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()

def step5(headers):
    print '-----step5-----'
    host = 'www.zj.10086.cn'
    del headers['Content-Length']
    del headers['Content-Type']
    del headers['Origin']
    del headers['Referer']
    headers['Cookie'] = cookie_manager.to_string()

    conn = httplib.HTTPConnection(host)
    req = conn.request('GET','/my/login/loginSuccess.do', headers = headers)
    res = conn.getresponse()
    cookie_manager.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()

def step7(headers):
    print '-----step7-----'
    host = 'www.zj.10086.cn'
    headers['Host'] = host
    headers['Cookie'] = cookie_manager.to_string()
    conn = httplib.HTTPConnection(host)
    req = conn.request('GET','/my/include/mybill.jsp', headers = headers)
    res = conn.getresponse()
    cookie_manager.update(res.getheader('set-cookie'))
    page = res.read()
    conn.close()
    m = re.search(r'http://service.zj.10086.cn/yw/bill/billDetail.do\?bid=([\w\d]+)&month=0', page)
    url = '/yw/bill/billDetail.do?bid=%s&month=0'%(m.groups()[0])
    return url

def step8(headers, url):
    print '-----step8-----'
    conn = httplib.HTTPConnection('service.zj.10086.cn')
    headers['Host'] = 'service.zj.10086.cn'
    headers['Cookie'] = cookie_manager.to_string()
    req = conn.request('GET',url, headers = headers)
    res = conn.getresponse()
    cookie_manager.update(res.getheader('set-cookie'))
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

def query_10086(phone, skip = False):
    try:
        headers = default_headers()
        if not skip:
            code = step1(headers)
            SAMLart = step2(headers, phone, code)
            if not SAMLart: return
            SAMLart = step3(headers, SAMLart)
            if not SAMLart: return
            step4(headers, SAMLart)
            step5(headers)
        url = step7(headers)
        return step8(headers, url)
    except Exception as e:
        print e
        pass

print query_10086('13429039463')
