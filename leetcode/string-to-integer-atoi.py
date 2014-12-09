#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import string
class Solution:
    # @return an integer
    def atoi(self, str):
        s = string.strip(str)
        if not s: return 0
        idx = 0
        if s[0] in "+-":
            if s[0] == '+':
                s = s[1:]
            else:
                idx = 1
        while idx < len(s) and s[idx] in "0123456789": idx += 1
        try:
            v = int(s[:idx])
        except Exception, e:
            # print e
            v = 0
        # integer overflow
        if v > 2 ** 31 - 1: return 2 ** 31 - 1
        if v < - (2 ** 31): return - (2 ** 31)
        return v

s = Solution()
print s.atoi('  -0012a42')
print s.atoi('  +0012a42')
print s.atoi('  +-0012a42')
