#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a list of lists of string
    def totalNQueens(self, n):
        ct = [0]
        def check(history, row, col):
            for (r, c) in history:
                if abs(row - r) == abs(col - c) or c == col:
                    return False
            return True
        def place(history, level):
            if level == n:
                ct[0] += 1
            else:
                for c in range(0, n):
                    if check(history, level, c):
                        place(history + [(level, c)], level + 1)
        init_history = []
        init_level = 0
        place(init_history, init_level)
        return ct[0]

s = Solution()
print s.totalNQueens(4)
