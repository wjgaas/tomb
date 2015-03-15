#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param nums, a list of integer
    # @param k, num of steps
    # @return nothing, please modify the nums list in-place.
    def rotate(self, nums, k):
        sz = len(nums)
        s = nums[0:sz - k][::-1] + nums[sz - k:][::-1]
        s = s[::-1]
        nums[:] = s

s = Solution()
nums = [1,2,3,4,5,6,7]
s.rotate(nums, 3)
print nums
