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
    ListNode* insertionSortList(ListNode* head) {
        if (head == NULL) return head;
        ListNode* h = head;
        ListNode* t = head -> next;
        h -> next = NULL;
        while(t) {
            ListNode* nt = t -> next;
            ListNode* pa = NULL;
            ListNode* pb = h;
            while(pb && t -> val > pb -> val) {
                pa = pb;
                pb = pb -> next;
            }
            t -> next = pb;
            if (pa == NULL) {
                h = t;
            } else {
                pa -> next = t;
            }
            t = nt;
        }
        return h;
    }
};

int main() {
    return 0;
}
