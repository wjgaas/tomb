#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param strs, a list of strings
    # @return a list of strings
    def anagrams(self, strs):
        def feature(s):
            d = [0] * 26
            for x in s: d[ord(x) - ord('a')] += 1
            return tuple(d)
        d = {}
        for s in strs:
            ft = feature(s)
            if ft in d:
                d[ft].append(s)
            else:
                d[ft] = [s]
        rs = []
        for (k,v) in d.items():
            if len(v) != 1:
                rs.extend(v)
        return rs

s = Solution()
print s.anagrams(['abc','cba','dca','acd','ace'])
