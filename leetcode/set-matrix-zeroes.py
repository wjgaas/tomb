#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param matrix, a list of lists of integers
    # RETURN NOTHING, MODIFY matrix IN PLACE.
    def setZeroes(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        rs = []
        cs = []
        for r in xrange(0, n):
            for c in xrange(0, m):
                if matrix[r][c] == 0:
                    rs.append(r)
                    cs.append(c)
        seen = -1
        for r in rs:
            if r == seen: continue
            seen = r
            # clear row
            for c in xrange(0, m): matrix[r][c] = 0
        seen = -1
        for c in cs:
            if c == seen: continue
            seen = c
            # clear column.
            for r in xrange(0, n): matrix[r][c] = 0

s = Solution()
matrix = [[1,2,3],
          [4,5,6],
          [0,1,2]]
s.setZeroes(matrix)
print matrix
