#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param A, a list of integers
    # @param target, an integer to be inserted
    # @return integer
    def searchInsert(self, A, target):
        s = 0
        e = len(A) - 1
        while s <= e:
            m = (s + e) / 2
            if A[m] > target: e = m - 1
            elif A[m] < target: s = m + 1
            else: return m
        return s
