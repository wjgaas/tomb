#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param matrix, a list of lists of integers
    # @return a list of integers
    def spiralOrder(self, matrix):
        n = len(matrix)
        if n == 0: return []
        m = len(matrix[0])
        if m == 0: return []

        ch = []
        for x in xrange(0, n): ch.append([0] * m)
        r = 0; c =0
        cnt = 0
        arr = 0 # 0 ->, 1 down, 2 <- 3, up
        rs = []
        while cnt != (n * m):
            # print r, c
            rs.append(matrix[r][c])
            ch[r][c] = 1
            cnt += 1
            def next(arr, (r, c)):
                if arr == 0: c += 1
                if arr == 1: r += 1
                if arr == 2: c -= 1
                if arr == 3: r -= 1
                return (r, c)
            # try next pos.
            (nr, nc) = next(arr, (r, c))
            if nc >= m or nc < 0 or nr >= n or nr < 0 or ch[nr][nc]:
                arr = (arr + 1) % 4
                (nr, nc) = next(arr, (r, c))
            (r, c) = (nr, nc)
        return rs

s = Solution()
matrix = [[1,2,3],[4,5,6],[7,8,9]]
print s.spiralOrder(matrix)
