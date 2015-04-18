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
    # @return a list node
    def detectCycle(self, head):
        p = head
        q = head
        t = None
        while p and q:
            p = p.next
            q = q.next
            if not q: return None
            q = q.next
            if p == q:
                t = p
                break
        if not t: return None
        # print 't =', t.val
        # determine cycle length.
        p = t
        n1 = 1
        p = p.next
        while p != t: p = p.next; n1 += 1
        # print 'cycle length', n1

        # distance from head to t.
        p = head
        n2 = 1
        while p != t: p = p.next; n2 += 1
        # print 'distance to t', n2

        h1 = t.next
        h2 = head
        if n1 <= n2:
            (h1, h2) = (h2, h1)
            (n1, n2) = (n2, n1)
        for i in range(0, n1 - n2): h1 = h1.next
        while h1 and h2:
            if h1 == h2:
                return h1
            h1 = h1.next
            h2 = h2.next
        assert(0)

s = Solution()
n1 = ListNode(1)
n2 = ListNode(2)
n3 = ListNode(3)
n4 = ListNode(4)

n1.next = n2; n2.next = n3; n3.next = n4
n4.next = n3
print s.detectCycle(n1).val

n4.next = n2
print s.detectCycle(n1).val

n4.next = n1
print s.detectCycle(n1).val

n4.next = n4
print s.detectCycle(n1).val
