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
    # @return the intersected ListNode
    def getIntersectionNode(self, headA, headB):
        def len_of_list(ls):
            size = 0
            while ls:
                size += 1
                ls = ls.next
            return size

        lenA = len_of_list(headA)
        lenB = len_of_list(headB)

        if lenA > lenB:
            (lenA, lenB) = (lenB, lenA)
            (headA, headB) = (headB, headA)
        # walk B lenB-lenA
        pa = headA
        pb = headB
        for i in range(0, lenB-lenA):
            pb = pb.next
        while pa and pb:
            if (pa == pb): return pa
            pa = pa.next
            pb = pb.next
        return None
