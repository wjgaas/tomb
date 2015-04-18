#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param matrix, a list of lists of integers
    # @param target, an integer
    # @return a boolean
    def searchMatrix(self, matrix, target):
        n = len(matrix)
        n2 = len(matrix[0])
        def find_row():
            s = 0
            e = n - 1
            while s <= e:
                m = (s + e) / 2
                if matrix[m][0] == target: return (True, -1)
                elif matrix[m][0] > target: e = m - 1
                else: s = m + 1
            return (False, e)
        (ok, r) = find_row()
        if ok: return ok
        def find_column():
            s = 0
            e = n2 - 1
            while s <= e:
                m = (s + e) / 2
                if matrix[r][m] == target: return True
                elif matrix[r][m] > target: e = m - 1
                else: s = m + 1
            return False
        return find_column()
