#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param S, a list of integer
    # @return a list of lists of integer
    def subsets(self, S):
        n = len(S)
        S.sort()
        rs = []
        def foo(idx, ss):
            if idx == n:
                rs.append(ss)
            else:
                foo(idx + 1, ss)
                foo(idx + 1, ss + [S[idx]])
        foo(0, [])
        return rs

S = [1,2,3]
s = Solution()
print s.subsets(S)
