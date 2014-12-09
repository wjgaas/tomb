#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

class Solution:
    # @param digits, a list of integer digits
    # @return a list of integer digits
    def plusOne(self, digits):
        n = len(digits) - 1
        carry = 1
        while n >= 0:
            digits[n] += carry
            if digits[n] >= 10:
                carry = 1
                digits[n] -= 10
            else:
                carry = 0
                break
            n -= 1
        if carry:
            digits.insert(0, carry)
        return digits

s = Solution()
print s.plusOne([9,9,9,9])
