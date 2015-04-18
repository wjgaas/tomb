#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param version1, a string
    # @param version2, a string
    # @return an integer
    def compareVersion(self, version1, version2):
        vs1 = version1.split('.')
        vs2 = version2.split('.')
        idx = 0
        while idx < len(vs1) or idx < len(vs2):
            if idx < len(vs1):
                i1 = int(vs1[idx])
            else:
                i1 = 0
            if idx < len(vs2):
                i2 = int(vs2[idx])
            else:
                i2 = 0
            if i1 < i2: return -1
            elif i1 > i2: return 1
            idx += 1
        return 0
