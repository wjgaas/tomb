#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from common import *
import traceback

def main():
    pid = os.getpid()
    cm = CookieManager(pid)
    vcode = VCode(pid)
    cp = ConnectionPool()
    pb = PhoneBalanceDB('input.db')
    headers = cp.default_headers()
    try:
        print '-----初始化cookie-----'
        initial_cookie(cm, cp, vcode, headers)
    except Exception as e:
        print '-----初始化cookie发生异常-----'
        traceback.print_exc()
        pass

    while True:
        p = pb.randomly_select_phone()
        if not p: print 'ALL DONE!!!'; break
        headers = cp.default_headers()
        try:
            print '-----获取验证码-----'
            initial_cookie(cm, cp, vcode, headers)
        except Exception as e:
            print '-----获取验证码发生异常-----'
            traceback.print_exc()
            continue
        vcode.show()
        vcode.input()
        try:
            print '-----查询余额-----'
            res = get_phone_balance(cm, cp, headers, p, vcode.code)
            if res:
                (balance, company, number) = res
                pb.update_phone_balance(p, balance)
                print "更新号码 '%s' = %s 成功" % (p, balance)
            else:
                print "更新号码 '%s' 失败" % (p)
        except Exception as e:
            print '-----查询余额发生异常-----'
            pass
main()
