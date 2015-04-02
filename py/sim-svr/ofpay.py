#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# 充值，查询充值状态，历史账单
# test sim no 1342904
# test phone no 13484095106
# test device no 130

import hashlib
import datetime
import urllib
import urllib2
import xml.dom.minidom
import traceback
import os
import MySQLdb
import redis
import json

kChargeUnknown = 255
kCharging = 0
kChargeOK = 1
kChargeFailed = 2
kChargeNoOrder = 3

from mysql_wrapper import MySQLWrapper
def creator_mysql_connection():
    return MySQLdb.connect(host = '127.0.0.1', user = 'autocube', passwd = 'autocube@2014', db = 'autocube', port = 3306)

class OFPayer:
    def __init__(self):
        self.pf = None
        self.mh = MySQLWrapper(creator_mysql_connection)
        self.rh = redis.StrictRedis(host = '127.0.0.1', port = 6379, db = 1)
        self.auto_id = 0
        self.pid = os.getpid()
        self.user_id = 'Axxxxx'
        m = hashlib.md5()
        m.update('<password>')
        self.user_pws = m.hexdigest()
        self.card_id = '140101' # 快充编号
        self.card_nums = [1,2,5,10,20,30,50,100,300] # 快充金额
        # todo(dirlt): 只有超过30元才收费金额才少于30.

    def parse_xml(self, s):
        # convert encoding.
        s = s.decode('GB2312').encode('UTF-8')
        s = s.replace('GB2312', 'UTF-8')
        root = xml.dom.minidom.parseString(s)
        order = root.getElementsByTagName('orderinfo')[0]
        kv = {}
        for c in order.childNodes:
            if c.nodeType == c.ELEMENT_NODE:
                k = c.tagName
                v = ''
                if c.childNodes: v = c.childNodes[0].data.encode('utf-8')
                kv[k] = v
        return kv

    def gen_uid(self):
        xid = self.auto_id
        self.auto_id += 1
        uid = '%d_%d' % (self.pid, xid)
        return uid

    def current_time(self):
        now = datetime.datetime.now()
        s0 = now.strftime('%Y%m%d%H%M%S')
        s1 = now.strftime('%Y-%m-%d %H:%M:%S')
        return (s0, s1)

    def pre_charge(self, sporder_id, sporder_ts, card_num, phone_no):
        if not card_num in self.card_nums: return False
        self.card_num = card_num
        self.sporder_id = sporder_id
        self.sporder_ts = sporder_ts
        self.sporder_time = sporder_ts[0]
        self.sporder_time2 = sporder_ts[1]
        self.phone_no = phone_no
        body = self.user_id + self.user_pws + self.card_id + str(self.card_num) + \
          self.sporder_id + self.sporder_time + phone_no + 'OFCARD'
        m = hashlib.md5()
        m.update(body)
        self.md5_str = m.hexdigest().upper()
        self.callback_url = urllib.quote('http://<host>/sim-svr/charge-cb')
        url = 'http://api2.ofpay.com/onlineorder.do?userid=%(user_id)s&userpws=%(user_pws)s&cardid=%(card_id)s&cardnum=%(card_num)s&sporder_id=%(sporder_id)s&sporder_time=%(sporder_time)s&game_userid=%(phone_no)s&md5_str=%(md5_str)s&ret_url=%(callback_url)s&version=6.0' % self.__dict__
        self.charge_url = url
        return True

    def request_url(self, url, xml = True, retry = 3):
        # todo(dirlt): 测试是否会重复充值
        # note(dirlt): 不会重复充值
        while retry:
            try:
                f = urllib2.urlopen(url)
                data = f.read()
                if xml: kv = self.parse_xml(data); return kv
                else: return data
            except Exception as e:
                retry -= 1
                traceback.print_exc()
                continue

    def do_charge(self):
        try:
            # 在数据库中建立一条新纪录
            orderid = '???'
            ordercash = 0.0
            st = kChargeUnknown
            ps = "INSERT IGNORE INTO phone_charge_history VALUES('%s', '%s', %s, '%s', '%s', %s, %s)" % (self.sporder_id, self.sporder_time2, self.card_num, self.phone_no, orderid, ordercash, st)
            self.mh.execute(ps, commit = True)
        except Exception as e:
            traceback.print_exc()
            # 如果数据库操作失败的话那么不会请求后端
            return
        # clear redis cache. 因为新增一条充值记录
        keys = self.rh.keys('pch_' + self.phone_no + '_*')
        for k in keys: self.rh.delete(k)
        return self.request_url(self.charge_url)

    def post_charge(self, kv):
        if not kv: return (-1, 'gateway error')
        if not 'retcode' in kv or kv['retcode'] != '1': return (-2, kv['err_msg'])
        if kv['game_state'] == '9': return (-3, 'charge failed') # 充值撤销
        st = int(kv['game_state']) # 0：充值中 1：成功
        # 更新充值状态.
        assert(st in (0, 1))
        orderid = kv['orderid']
        ordercash = kv['ordercash']
        ps = "UPDATE phone_charge_history SET orderid = '%s', ordercash = '%s', orderst = %s WHERE spid = '%s'" % (orderid, ordercash, st, self.sporder_id)
        self.mh.execute(ps, commit = True)
        if st == 0: return (0, 'charging')
        else: return (1, 'done')

    def query_charge_status(self, sporder_id):
        url = 'http://api2.ofpay.com/api/query.do?userid=%s&spbillid=%s' % (self.user_id, sporder_id)
        data = self.request_url(url, False)
        st = int(data)
        return st

    def update_charge_status(self, sporder_id, st):
        if not st: return False
        # 0: ing,  1: done,  -1: no order, 9: failed.
        if st == -1: st = kChargeNoOrder
        elif st == 9: st = kChargeFailed
        ps = "UPDATE phone_charge_history SET orderst = %s WHERE spid = '%s'" % (st, sporder_id)
        self.mh.execute(ps, commit = True)
        # 状态是否稳定
        if st == 0: return False
        return True

    def query_charge_history(self, phone_no, period = 30, limit = 10):
        # todo(dirlt): 是否需要在这里有所限制. 比如我们只查询最近3,10,30天充值纪录，限制返回上限在10个
        k = 'pch_' + phone_no + '_%s_%s' % (period, limit)
        s = self.rh.get(k)
        if s: return s

        # 查询最近3次是否有正在充值的记录，如果有的话立刻更新状态
        # 通常来说是用户希望查询自己充值是否成功
        ps = "SELECT spid FROM phone_charge_history WHERE phone_no = '%s' AND orderst = 0 ORDER BY sptime DESC LIMIT 3" % (phone_no)
        cur = self.mh.execute(ps)
        rs = cur.fetchall()
        cur.close()
        if not rs: rs = []
        stable = True
        for r in rs:
            spid = r[0]
            st = self.query_charge_status(spid)
            stable &= self.update_charge_status(spid, st)
        # 然后用户来查询充值状态. 默认最近一个月，限制查询最近10条
        # 只查询 充值完成 和 正在充值
        ps = "SELECT sptime, orderid, orderst FROM phone_charge_history WHERE phone_no = '%s' AND DATEDIFF(sptime, NOW()) <= %s AND (orderst = 0 OR orderst = 1) ORDER BY sptime DESC LIMIT %s" % (phone_no, period, limit)
        res = []
        cur = self.mh.execute(ps)
        rs = cur.fetchall()
        if not rs: rs = []
        for r in rs:
            (sptime, orderid, orderst) = r
            sptime = sptime.strftime('%Y-%m-%d %H:%M:%S')
            res.append((orderid, sptime, orderst))
        cur.close()
        s = json.dumps(res)
        if stable: self.rh.setex(k, 10 * 60, s) # 缓存10分钟
        return s

    def complete_history(self):
        ps = "SELECT spid FROM phone_charge_history WHERE orderst = 0 ORDER BY sptime;"
        cur = self.mh.execute(ps)
        while True:
            rs = cur.fetchmany(100)
            if not rs: cur.close(); break
            for r in rs:
                spid = r[0]
                st = self.query_charge_status(spid)
                self.update_charge_status(spid, st)
        self.mh.close()

def test():
    p = OFPayer()
    uid = 'test00014'
    phone = '13484095106'

    # # 充值
    # ts = p.current_time()
    # p.pre_charge(uid, ts, 2, phone)
    # kv = p.do_charge()
    # print p.post_charge(kv)

    # 查询充值记录
    print p.query_charge_history(phone)

if __name__ == '__main__':
    test()
