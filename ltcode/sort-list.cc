/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

#include <cstdio>
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode* sortList(ListNode* head) {
        ListNode* p = head;
        int len = 0;
        while(p) {
            len ++;
            p = p -> next;
        }
        return sortList(head, len);
    }
    ListNode* sortList(ListNode* head, int len) {
        if(len == 0 || len == 1) return head;
        ListNode* t = head;
        for(int i = 1; i < (len >> 1); i++) t = t->next;

        // two separate lists.
        ListNode* pa = head; // len >> 1
        ListNode* pb = t -> next; // len - (len >> 1)
        t -> next = NULL;
        pa = sortList(pa, len >> 1);
        pb = sortList(pb, len - (len >> 1));

        // merge them.
        ListNode* xa = NULL;
        ListNode* xt = NULL;
        while(pa && pb) {
            if (pa -> val < pb -> val) {
                t = pa;
                pa = pa -> next;
            } else {
                t = pb;
                pb = pb -> next;
            }
            if (xa == NULL) {
                xa = t;
            } else {
                xt -> next = t;
            }
            xt = t;
            xt -> next = NULL;
        }
        t = pa ? pa : pb;
        if (xa == NULL) {
            return t;
        } else {
            xt -> next = t;
            return xa;
        }
    }
};

int main() {
    Solution s;
    {
        ListNode t1(1);
        ListNode t2(2);
        t1.next = &t2;
        ListNode* p = s.sortList(&t1);
    }
    return 0;
}
