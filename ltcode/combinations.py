#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a list of lists of integers
    def combine(self, n, k):
        rs = []
        def foo(idx, ss):
            if len(ss) == k:
                rs.append(ss)
            else:
                if (idx == n): return
                foo(idx + 1, ss)
                foo(idx + 1, ss + [idx + 1])
        foo(0, [])
        return rs

s = Solution()
print s.combine(4, 2)
