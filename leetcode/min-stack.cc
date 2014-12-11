#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <algorithm>

class MinStack {
  public:
    struct node {
        int val : 8;
        int mnv : 8;
    } __attribute__((packed));
    struct node* pool;
    int head;
    static const int N = 70001;

    MinStack() {
        pool = (struct node*) malloc (sizeof(struct node) * N);
        head = -1;
    }
    ~MinStack() {
        free(pool);
    }

    void push(int x) {
        struct node* p = &pool[head + 1];
        p->val = x;
        if (head == -1) {            
            p->mnv = x;
        } else {
            struct node* pp = &pool[head];
            p->mnv = std::min(x, pp->mnv);
        }
        head++;
        if (head == N) assert(0);
    }

    void pop() {        
        if (head == -1) return ;
        head--;
    }

    int top() {
        if (head == -1) return -1;
        return pool[head].val;
    }

    int getMin() {
        if (head == -1) return -1;
        return pool[head].mnv;
    }
};

int main() {
    printf("sizeof(node) = %zu\n", sizeof(MinStack::node));
    
    MinStack s;
    s.push(5); s.push(7); s.push(8);
    s.push(3); s.push(4);
    printf("%d %d\n", s.getMin(), s.top());
    s.pop(); s.pop();
    printf("%d %d\n", s.getMin(), s.top());
    s.pop(); s.pop(); s.pop();
    printf("%d %d\n", s.getMin(), s.top());

    int A[] = {10, 30, 20, 60, 5, 25};
    int C[] = {1, 0, 0, 0, 1, 0};
    for (int i = 0; i< 6; i++) {
        s.push(A[i]);
        if (C[i]) {
            s.pop();
        }
        printf("%d\n", s.top());
    }
    return 0;
}
