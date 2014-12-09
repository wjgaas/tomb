#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param candidates, a list of integers
    # @param target, integer
    # @return a list of lists of integers
    def combinationSum(self, candidates, target):
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
            cnt = 0
            rs = []
            while target >= cnt * v:
                ss = foo(candidates, s + 1, target - cnt * v)
                base = [v] * cnt
                for x in ss: rs.append(base + x)
                cnt += 1
            cache[key] = rs
            return cache[key]

        return foo(candidates, 0, target)

s = Solution()
print s.combinationSum([2,3,6,7], 7)
