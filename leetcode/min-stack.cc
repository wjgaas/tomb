#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <algorithm>
#include <deque>

#if 0
// MLE.
class MinStack {
  public:
    struct node {
        int val : 20;
        int mnv : 20;
    } __attribute__((packed));
    struct node* pool;
    int head;
    static const int N = 70001;

    MinStack() {
        printf("sizeof(node) = %zu\n", sizeof(struct node));
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

// MLE.
class MinStack {
  public:
    typedef long long val_type;
    struct node {
        val_type val : 48;
    } __attribute__((packed));
    struct node* pool;
    int head;
    val_type minv;
    static const int N = 70001;

    MinStack() {
        printf("sizeof(node) = %zu\n", sizeof(struct node));
        pool = (struct node*) malloc (sizeof(struct node) * N);
        head = -1;
    }
    ~MinStack() {
        free(pool);
    }

    void push(int x) {
        if (head == -1) {
            pool[++head].val = 0;
            minv = x;
        } else {
            // neg value implies minv is changed.
            pool[++head].val = (val_type)x - minv;
            minv = std::min(minv, (val_type)x);
        }
        if (head == N) assert(0);
    }

    void pop() {
        if (head == -1) return ;
        val_type x = pool[head--].val;
        // x - (x - last_minv)
        if (x < 0) minv = minv - x;
    }

    int top() {
        if (head == -1) return -1;
        val_type x = pool[head].val;
        if (x < 0) return minv;
        else return minv + x;
    }

    int getMin() {
        if (head == -1) return -1;
        return minv;
    }
};
#endif

// don't allocate pair for all cases.
class MinStack {
  private:
    std::deque<int> st;
    std::deque<int> mi;
  public:
    void push(int x) {
        st.push_back(x);
        if (mi.empty() || x <= mi.back()) mi.push_back(x);
    }

    void pop() {
        if (st.empty()) return;
        if (st.back() == mi.back()) mi.pop_back();
        st.pop_back();
    }

    int top() {
        if (st.empty()) return -1;
        return st.back();
    }

    int getMin() {
        if (mi.empty()) return -1;
        return mi.back();
    }
};

int main() {
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
