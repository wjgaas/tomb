#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A, a list of integers
    # @return an integer
    def maxSubArray(self, A):
        def conquer(array, pivot):
            # (s, pivot-1), (pivot, e)
            s = 0; e = len(array) - 1
            L = array[pivot-1]; R = array[pivot]
            y = 0
            for i in xrange(pivot-1, s-1, -1):
                y += array[i]
                L = max(L, y)
            y = 0
            for i in xrange(pivot, e+1):
                y += array[i]
                R = max(R, y)
            return max(L, R, L+R)

        def divide(array):
            n = len(array)
            if n == 1: return array[0]
            pivot = n / 2
            L = divide(array[:pivot])
            R = divide(array[pivot:])
            y = conquer(array, pivot)
            return max(L, R, y)

        return divide(A)

s = Solution()
print s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
