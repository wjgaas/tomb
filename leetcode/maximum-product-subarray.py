#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A, a list of integers
    # @return an integer
    def maxProduct(self, A):
        def conquer(array, pivot):
            # (s, pivot-1), (pivot, e)
            s = 0; e = len(array) - 1
            (lmn, lmx) = (array[pivot-1], array[pivot-1])
            (rmn, rmx) = (array[pivot], array[pivot])
            y = 1
            for i in xrange(pivot-1, s-1, -1):
                y *= array[i]                                
                lmn = min(lmn, y)
                lmx = max(lmx, y)
            y = 1
            for i in xrange(pivot, e+1):
                y *= array[i]
                rmn = min(rmn, y)
                rmx = max(rmx, y)            
            return (max(lmx, rmx, lmn * rmn, lmx * rmx),
                    min(lmn, rmn, lmn * rmx, lmx * rmn))

        def divide(array):
            n = len(array)
            if n == 1: return array[0]
            pivot = n / 2
            lmx = divide(array[:pivot])
            rmx = divide(array[pivot:])
            (mx, _) = conquer(array, pivot)
            return max(lmx, rmx, mx)

        return divide(A)

s = Solution()
# print s.maxProduct([2,3,-2,4])
print s.maxProduct([-2,3,-4])
