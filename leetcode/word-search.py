#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param board, a list of lists of 1 length string
    # @param word, a string
    # @return a boolean
    def exist(self, board, word):
        n = len(board)
        m = len(board[0])
        wn = len(word)
        mask = []
        for i in range(0, n):
            mask.append([0] * m)
        
        def dfs(loc, seen):
            (r, c) = loc
            sn = len(seen)

            if sn == wn and seen == word: return True
            if sn >= wn: return False
                
            ps = []
            if r > 0: ps.append((r-1, c))
            if c > 0: ps.append((r, c-1))
            if r < (n-1): ps.append((r+1, c))
            if c < (m-1): ps.append((r, c+1))
            for p in ps:
                (pr, pc) = p
                if mask[pr][pc]: continue
                if not board[pr][pc] == word[sn]: continue
                mask[pr][pc] = 1
                if dfs(p, seen + word[sn]):
                    return True
                mask[pr][pc] = 0
            return False

        for r in range(0, n):
            for c in range(0, m):
                if board[r][c] == word[0]:
                    mask[r][c] = 1
                    if dfs((r,c), word[0]):
                        return True
                    mask[r][c] = 0
        return False
    
s = Solution()
board = ["aaaa", "aaaa", "aaaa"]
word = "aaaaaaaaaaa"
board = ["a"]
word = "a"
print s.exist(board, word)            
