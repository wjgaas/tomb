#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a list of lists of integer
    def generateMatrix(self, n):
        ch = []
        for x in xrange(0, n): ch.append([0] * n)
        r = 0; c =0
        cnt = 0
        arr = 0 # 0 ->, 1 down, 2 <- 3, up
        d = 1
        while cnt != (n * n):
            ch[r][c] = d
            # print r,c
            d += 1
            cnt += 1
            def next(arr, (r, c)):
                if arr == 0: c += 1
                if arr == 1: r += 1
                if arr == 2: c -= 1
                if arr == 3: r -= 1
                return (r, c)
            # try next pos.
            (nr, nc) = next(arr, (r, c))
            if nc >= n or nc < 0 or nr >= n or nr < 0 or ch[nr][nc]:
                arr = (arr + 1) % 4
                (nr, nc) = next(arr, (r, c))
            (r, c) = (nr, nc)
        return ch

s = Solution()
print s.generateMatrix(1)
print s.generateMatrix(3)
