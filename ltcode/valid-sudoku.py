#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param board, a 9x9 2D array
    # @return a boolean
    def isValidSudoku(self, board):
        def ok(mk):
            for x in mk:
                if x > 1: return False
            return True
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                mk = [0] * 10
                for i in range(0, 3):
                    for j in range(0, 3):
                        v = board[r + i][c + j]
                        if v != '.':
                            mk[ord(v) - ord('0')] +=1
                if not ok(mk): return False
        for r in range(0, 9):
            mk = [0] * 10
            for c in range(0, 9):
                v = board[r][c]
                if v != '.': mk[ord(v) - ord('0')] += 1
                if not ok(mk): return False
            mk = [0] * 10
            for c in range(0, 9):
                v = board[c][r]
                if v !='.': mk[ord(v) - ord('0')] += 1
                if not ok(mk): return False
        return True

board = [['.'] * 9]  * 9
print board
s = Solution()
print s.isValidSudoku(board)
