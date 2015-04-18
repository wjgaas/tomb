#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param matrix, a list of lists of integers
    # @return a list of lists of integers
    def rotate(self, matrix):
        n = len(matrix)
        for r in range(0, n / 2 + 1):
            for c in range(r, n - r - 1):
                p1 = (r, c)
                p2 = (c, n - 1 - r)
                p3 = (n - 1 - r, n - 1 - c)
                p4 = (n - 1 - c, r)
                # (p2, p3, p4, p1) = (p1, p2, p3, p4)
                v = map(lambda x: matrix[x[0]][x[1]], (p1, p2, p3, p4))
                xx = zip((p2, p3, p4, p1), v)
                for p, v in xx:
                    matrix[p[0]][p[1]] = v
        return matrix

s = Solution()
matrix = [[1,2],[3,4]]
print s.rotate(matrix)
