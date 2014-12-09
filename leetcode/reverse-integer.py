#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return an integer
    def reverse(self, x):
        minus = False
        if x < 0: minus = True
        x = abs(x)
        s = str(x)[::-1]
        x = int(s)
        if minus: x = -x
        # integer overflow
        if x > 2 ** 31 - 1 or x < -(2 ** 31): return 0
        return x

s = Solution()
print s.reverse(1534236469)
