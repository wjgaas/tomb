#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a string
    def convert(self, s, nRows):
        ns = ''
        n = len(s)
        if nRows == 1 or n <= nRows: return s
        for r in xrange(0, nRows):
            idx = r
            ns += s[idx]
            # print idx
            while idx < n:
                idx += 2 * (nRows - 1)
                if not (r == 0 or r == (nRows - 1)):
                    if ((idx - 2 * r) < n):
                        # print idx - 2 * r
                        ns += s[idx - 2 * r]
                if idx < n:
                    # print idx
                    ns += s[idx]
        return ns

s = Solution()
# print s.convert("PAYPALISHIRING", 3)
print s.convert("ABCDEFGHIJ", 4)
