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
    # @param x, an integer
    # @return a ListNode
    def partition(self, head, x):
        h1 = [None, None]
        h2 = [None, None]
        def add_tail(h, p):
            if not h[0]:
                h[0] = p
                h[1] = p
            else:
                h[1].next = p
                h[1] = p
        p = head
        while p:
            if p.val < x: add_tail(h1, p)
            else: add_tail(h2, p)
            np = p.next
            p.next = None
            p = np
        add_tail(h1, h2[0])
        return h1[0]
        
