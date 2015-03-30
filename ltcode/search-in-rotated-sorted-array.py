#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A, a list of integers
    # @param target, an integer to be searched
    # @return an integer
    def search(self, A, target):
        s = 0
        e = len(A) - 1
        while s <= e:
            m = (s + e) / 2
            if A[m] == target: return m
            if A[m] <= A[e]:
                if target > A[m] and target <= A[e]:
                    s = m + 1
                else:
                    e = m - 1
            else:
                if target < A[m] and target >= A[s]:
                    e = m - 1
                else:
                    s = m + 1
        return -1

s = Solution()
print s.search([4,5,6,7,0,1,2], 1)
print s.search([4,5,6,7,0,1,2], 2)
print s.search([4,5,6,7,0,1,2], 8)
