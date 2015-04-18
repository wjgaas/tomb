#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # @param head, a ListNode
    # @param k, an integer
    # @return a ListNode
    def reverseKGroup(self, head, k):
        def push_node(st, p):
            if st[0] == None:
                st[0] = p
                st[1] = p
                p.next = None
            else:
                p.next = st[0]
                st[0] = p
        def push_st(ht, st):
            if ht[0] == None:
                ht[0] = st[0]
                ht[1] = st[1]
            else:
                ht[1].next = st[0]
                ht[1] = st[1]
            st[:] = [None, None]

        ht = [None, None]
        st = [None, None]
        p = head
        while p:
            sp = p
            cnt = 0
            while sp and cnt < k:
                #print 'push', sp.val
                tp = sp.next
                push_node(st, sp)
                cnt += 1
                sp = tp
            p = sp                
            if cnt == k:
                #print 'push st'
                push_st(ht, st)
            else:
                # reverse back.
                t = st[0]
                st = [None, None]
                while t: tt = t.next; push_node(st, t); t = tt
                push_st(ht, st)                
        return ht[0]

def make_list(vals):
    head = ListNode(vals[0])
    tail = head
    for x in vals[1:]:
        p = ListNode(x)
        tail.next = p
        tail = p
    return head

def print_list(ls):
    p = ls
    cnt = 20
    while p and cnt > 0: print p.val,; p = p.next; cnt -= 1
    print ''

s = Solution()
h = [1,2,3,4,5]
print_list (s.reverseKGroup(make_list(h), 2))
print_list (s.reverseKGroup(make_list(h), 3))
