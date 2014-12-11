#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a string
    def getPermutation(self, n, k):
        seq = ''
        ns = []
        for x in xrange(1, n+1): ns.append(x)
        def fac(x):
            prod = 1
            for i in xrange(1, x+1): prod *= i
            return prod
        k = (k - 1) % fac(n)
        while len(ns) > 1:
            base = fac(len(ns) - 1)
            pos = k / base
            k %= base
            seq += str(ns[pos])
            ns.remove(ns[pos])
        seq += str(ns[0])
        return seq

s = Solution()
print s.getPermutation(3, 1)
print s.getPermutation(3, 2)
print s.getPermutation(3, 3)
print s.getPermutation(2, 2)
