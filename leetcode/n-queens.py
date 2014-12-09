#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @return a list of lists of string
    def solveNQueens(self, n):
        ss = []
        def check(history, row, col):
            for (r, c) in history:
                if abs(row - r) == abs(col - c) or c == col:
                    return False
            return True
        def place(history, level):
            if level == n:
                ss.append(history)
            else:
                for c in range(0, n):
                    if check(history, level, c):
                        place(history + [(level, c)], level + 1)
        init_history = []
        init_level = 0
        place(init_history, init_level)

        def interpret(s):
            rep = []
            for i in range(0, n):
                sr = ''
                for j in range(0, n):
                    if j == s[i][1]:
                        sr += 'Q'
                    else:
                        sr += '.'
                rep.append(sr)
            return rep

        ret = []
        for s in ss:
            ret.append(interpret(s))
        return ret

s = Solution()
print s.solveNQueens(4)
