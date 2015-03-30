#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param n, an integer
    # @return an integer
    # fib number
    def climbStairs(self, n):
        f0 = 1
        f1 = 1
        idx = 2
        while idx <= n:
            (f1, f0) = (f0 + f1, f1)
            idx += 1
        return f1

s = Solution()
print s.climbStairs(3)
