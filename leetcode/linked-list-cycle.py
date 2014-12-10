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
    # @return a boolean
    def hasCycle(self, head):
        p = head
        q = head
        while p and q:
            p = p.next
            q = q.next
            if not q: return False
            q = q.next
            if p == q: return True
        return False
