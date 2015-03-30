#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A a list of integers
    # @param target an integer
    # @return a boolean
    def search(self, A, target):
        s = 0
        e = len(A) - 1
        if A[s] == target: return True
        # if A[s] == A[e], we have to search leftmost p
        # where A[p] != A[e], but A[p+1] == A[e]
        while e >= 0 and A[e] == A[s]: e -= 1
        while s <= e:
            m = (s + e) / 2
            if A[m] == target: return True
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
        return False

s = Solution()
print s.search([4,5,6,7,0,1,2], 1)
print s.search([4,5,6,7,0,1,2], 2)
print s.search([4,5,6,7,0,1,2], 8)
print s.search([1,1,3,1], 3)
