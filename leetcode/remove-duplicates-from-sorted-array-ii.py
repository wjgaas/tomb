#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A a list of integers
    # @return an integer
    def removeDuplicates(self, A):
        n = len(A)
        if n in (0, 1): return n
        seen = A[0]
        dup = 1
        ns = []
        for x in A[1:]:
            if x == seen:
                dup += 1
            else:
                ns += [seen] * min(dup, 2)
                seen = x
                dup = 1
        ns += [seen] * min(dup, 2)
        A[:] = ns
        return len(ns)
