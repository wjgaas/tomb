#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a string
    def countAndSay(self, n):
        def trans(s):
            n = len(s)
            ns = ''


            cnt = 1
            seen = s[0]
            idx = 1
            while idx < n:
                while idx < n and s[idx] == seen: cnt += 1; idx += 1
                ns += str(cnt)
                ns += str(seen)
                if idx == n:
                    cnt = 0
                    break
                seen = s[idx]
                cnt = 1
                idx += 1
            if cnt:
                ns += str(cnt)
                ns += str(seen)
            return ns

        s = '1'
        for i in range(1, n):
            x = trans(s)
            # print 'iter#%d = %s'%(i+1, x)
            s = x
        return s

s = Solution()
print s.countAndSay(8)
