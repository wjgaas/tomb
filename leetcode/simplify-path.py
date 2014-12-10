#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import string
class Solution:
    # @param path, a string
    # @return a string
    def simplifyPath(self, path):
        ss = string.split(path, '/')
        ns = []
        for s in ss:
            if not s or s == '.': continue
            elif s == '..':
                if ns: ns = ns[:-1]
            else: ns.append(s)
        return '/' + string.join(ns, '/')

s = Solution()
# print s.simplifyPath("/a/./b/../../c/")
# print s.simplifyPath('/home/')
# print s.simplifyPath('/..')
# print s.simplifyPath('/../../')
print s.simplifyPath("/a/./b///../c/../././../d/..//../e/./f/./g/././//.//h///././/..///")
