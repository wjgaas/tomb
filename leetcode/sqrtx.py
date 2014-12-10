#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param x, an integer
    # @return an integer
    def sqrt(self, x):
        if x in (0, 1): return x
        s = 1
        e = x
        while s <= e:
            m = (s + e) / 2
            m2 = m * m
            if m2 > x: e = m - 1
            elif m2 < x: s = m + 1
            else:
                return m
        return e
