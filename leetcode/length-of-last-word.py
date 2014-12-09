#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import string
class Solution:
    # @param s, a string
    # @return an integer
    def lengthOfLastWord(self, s):
        ss = string.split(string.strip(s), ' ')
        if len(ss) == 0 : return 0
        return len(ss[-1])

s = Solution()
print s.lengthOfLastWord('   ')
print s.lengthOfLastWord('Hello World ')
print s.lengthOfLastWord('Hello World')
