#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import itertools
class Solution:
    # @param num, a list of integer
    # @return a list of lists of integers
    def permute(self, num):
        rs = []
        for r in itertools.permutations(num):
            rs.append(list(r))
        return rs

s = Solution()
print s.permute([1,2,3])
