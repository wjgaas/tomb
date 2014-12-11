#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param obstacleGrid, a list of lists of integers
    # @return an integer
    def uniquePathsWithObstacles(self, obstacleGrid):
        n = len(obstacleGrid);
        m = len(obstacleGrid[0])
        mask = []
        for i in xrange(0, n): mask.append([0] * m)
        ret = [0]

        def dfs(p):
            if p == (n-1, m-1): ret[0] +=1; return
            (r, c) = p
            mask[r][c] = 1
            if r != (n-1) and obstacleGrid[r+1][c] == 0 and mask[r+1][c] == 0:
                mask[r+1][c] = 1
                dfs((r+1, c))
                mask[r+1][c] = 0
            if c != (m-1) and obstacleGrid[r][c+1] == 0 and mask[r][c+1] == 0:
                mask[r][c+1] = 1
                dfs((r, c+1))
                mask[r][c+1] = 0

        dfs((0, 0))
        return ret[0]

obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
s = Solution()
print s.uniquePathsWithObstacles(obstacleGrid)
