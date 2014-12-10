#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param grid, a list of lists of integers
    # @return an integer
    def minPathSum(self, grid):
        n = len(grid)
        m = len(grid[0])
        cache = []
        for i in xrange(0, n):
            cache.append([-1] * m)

        for i in xrange(0, n):
            for j in xrange(0, m):
                if i == 0 and j == 0: cache[i][j] = 0
                elif i > 0 and j > 0:
                    cache[i][j] = min(cache[i-1][j], cache[i][j-1])
                elif i > 0:
                    cache[i][j] = cache[i-1][j]
                elif j > 0:
                    cache[i][j] = cache[i][j-1]
                cache[i][j] += grid[i][j]
        return cache[n-1][m-1]
