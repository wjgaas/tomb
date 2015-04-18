#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param candidates, a list of integers
    # @param target, integer
    # @return a list of lists of integers
    def combinationSum2(self, candidates, target):
        cache = {}
        candidates.sort()
        n = len(candidates)

        def foo(candidates, s, target):
            if (target < 0): return []
            if s == n:
                if target == 0 : return [[]]
                else: return []

            key = '%d-%d'%(s, target)
            if key in cache: return cache[key]

            v = candidates[s]
            ns = s
            while ns < n and candidates[ns] == v: ns += 1
            idx = s

            rs = []
            while idx < n and candidates[idx] == v:
                ss = foo(candidates, ns, target - (idx - s + 1) * v)
                base = [v] * (idx - s + 1)
                for x in ss: rs.append(base + x)
                idx += 1
            ss = foo(candidates, ns, target)
            for x in ss: rs.append(x)
            cache[key] = rs
            return cache[key]

        return foo(candidates, 0, target)

s = Solution()
print s.combinationSum2([10,1,2,7,6,1,5], 8)
