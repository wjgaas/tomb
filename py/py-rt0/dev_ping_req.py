#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from worker import *

import sys
sys.path.append('../scripts/')
from dev_ping_req_pb2 import *

def print_pb(msg, st):
    req = DevPingRequest()
    req.ParseFromString(msg)
    print req

def cc(): return create_consumer(('dev-ping',), ['localhost:9092'], 'dev-ping-c0')
run_worker(cc, print_pb, None, debug = True)
