#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param obstacleGrid, a list of lists of integers
    # @return an integer
    def uniquePathsWithObstacles(self, obstacleGrid):
        n = len(obstacleGrid);
        m = len(obstacleGrid[0])
        dp = []
        dp.append([0] * m)
        dp.append([0] * m)
        sw = 0
        for i in xrange(0, n):
            for j in xrange(0, m):
                if obstacleGrid[i][j] == 1:
                    dp[sw][j] = 0
                else:
                    if i == 0 and j == 0: dp[sw][0] = 1
                    elif i == 0: dp[sw][j] = dp[sw][j-1]
                    elif j == 0: dp[sw][j] = dp[1-sw][j]
                    else: dp[sw][j] = dp[sw][j-1] + dp[1-sw][j]
                #print '(%d,%d) = %d'%(i, j, dp[sw][j])
            sw = 1 - sw
        return dp[1-sw][m-1]

obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
s = Solution()
print s.uniquePathsWithObstacles(obstacleGrid)
