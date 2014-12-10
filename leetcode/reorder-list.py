#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# class Solution:
#     # @param head, a ListNode
#     # @return nothing
#     def reorderList(self, head):
#         nh = [None]
#         nt = [None]
#         def add_to_tail(p):
#             # print 'add', p.val
#             if nh[0] == None:
#                 nh[0] = p
#                 nt[0] = p
#             else:
#                 nt[0].next = p
#                 nt[0] = p
#         def get_last(p):
#             pp = p
#             p = p.next
#             while p and p.next:
#                 pp = p
#                 p = p.next
#             return (pp, p)
#         while head:
#             p = head
#             (pp, last) = get_last(p)
#             pp.next = None
#             head = head.next
#             add_to_tail(p)
#             if last: add_to_tail(last)
#         return nh[0]

class Solution:
    # @param head, a ListNode
    # @return nothing
    def reorderList(self, head):
        n = 0
        p = head
        while p:
            n += 1
            p = p.next
        # special case.
        if n == 0 or n == 1: return head

        # locate (n-1)/2th elements.
        h1 = head
        p = head
        for i in xrange(0, (n-1)/2): p = p.next
        # print 'pivot = ', p.val
        sp = p.next
        p.next = None

        # reverse next elements.
        pp = None
        p = sp
        # print 'next pivot = ', p.val
        while p.next:
            np = p.next
            p.next = pp
            pp = p
            p = np
        p.next = pp
        h2 = p

        nh = h1
        nt = h1
        # print 'add', h1.val
        h1 = h1.next
        while h1 and h2:
            # print 'add', h2.val
            nt.next = h2
            nt = h2
            h2 = h2.next
            # print 'add', h1.val
            nt.next = h1
            nt = h1
            h1 = h1.next
        nt.next = h2
        # while h2: print 'add', h2.val; h2 = h2.next
        return nh

def make_list(vals):
    if len(vals) == 0: return None
    head = ListNode(vals[0])
    p = head
    for x in vals[1:]:
        n = ListNode(x)
        p.next = n
        p = n
    return head

def print_list(ls):
    while ls: print ls.val, ; ls = ls.next
    print ''

s = Solution()
print '-----'
s.reorderList(make_list([1]))
print '-----'
s.reorderList(make_list([1,2]))
print '-----'
print_list (s.reorderList(make_list([1,2,3])))
print '-----'
s.reorderList(make_list([1,2,3,4]))
print '-----'
s.reorderList(make_list([1,2,3,4,5]))
