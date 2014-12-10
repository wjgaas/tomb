#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return an integer
    def uniquePaths(self, m, n):
        # C(m + n , n)
        def fac(x):
            prod = 1
            for i in xrange(1, x+1): prod *= i
            return prod
        m -= 1
        n -= 1
        return fac(m + n) / fac(m) / fac(n)
