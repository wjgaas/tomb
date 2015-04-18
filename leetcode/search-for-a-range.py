#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A, a list of integers
    # @param target, an integer to be searched
    # @return a list of length 2, [index1, index2]
    def searchRange(self, A, target):
        n = len(A)
        def p1(a, t): return a >= t
        def p2(a, t): return a > t
        def g1(s, e): return s
        def g2(s, e): return e
        def search(pred, get):
            s = 0
            e = n - 1
            while s <= e:
                m = (s + e) / 2
                if pred(A[m], target): e = m - 1
                else: s = m + 1
            return get(s, e)

        idx1 = search(p1, g1)
        idx2 = search(p2, g2)
        if idx1 < 0 or idx1 >= n or A[idx1] != target: idx1 = -1
        if idx2 < 0 or idx2 >= n or A[idx2] != target: idx2 = -1
        return [idx1, idx2]

s = Solution()
print s.searchRange([5, 7, 7, 8, 8, 10], 8)
print s.searchRange([5, 7, 7, 8, 8, 10], 11)
print s.searchRange([5, 7, 7, 8, 8, 10], 4)
print s.searchRange([5, 7, 7, 8, 8, 10], 6)
