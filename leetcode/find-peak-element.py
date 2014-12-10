#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param num, a list of integer
    # @return an integer
    def findPeakElement(self, num):
        n = len(num)
        if n in (0, 1): return n-1
        for i in xrange(0, n):
            if (i == 0 and num[i] > num[i+1]) or \
                (i == (n-1) and num[i] > num[i-1]) or \
                (num[i] > num[i+1] and num[i] > num[i-1]):
                 return i
        assert(0)

s = Solution()
print s.findPeakElement([1,2,3,4,5,6,7])
