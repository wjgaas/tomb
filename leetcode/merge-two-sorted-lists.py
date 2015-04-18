#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # @param two ListNodes
    # @return a ListNode
    def mergeTwoLists(self, l1, l2):
        head = [None]
        tail = [None]
        def add_to_tail(p):
            if head[0] == None:
                head[0] = p
                tail[0] = p
            else:
                tail[0].next = p
                tail[0] = p

        p1 = l1
        p2 = l2
        while p1 and p2:
            if p1.val < p2.val:
                add_to_tail(p1)
                p1 = p1.next
            else:
                add_to_tail(p2)
                p2 = p2.next
        if p1: add_to_tail(p1)
        if p2: add_to_tail(p2)
        return head[0]
