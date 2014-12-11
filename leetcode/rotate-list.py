#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # @param head, a ListNode
    # @param k, an integer
    # @return a ListNode
    def rotateRight(self, head, k):
        sz = 0
        pp = None
        p = head
        while p:
            sz += 1
            pp = p
            p = p.next
        last = pp

        if sz == 0 or k % sz == 0: return head
        k %= sz
        ht = head
        p = head
        for i in xrange(0, sz - k - 1): p = p.next
        first = p.next

        # [ht, p] [first, last]
        last.next = ht
        p.next = None
        return first
