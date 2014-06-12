#include <cstdio>
#include <cassert>
#include <map>
using namespace std;

struct Node {
    int key;
    int value;
    struct Node* prev;
    struct Node* next;
    Node(int k, int v) : key(k), value(v), prev(NULL), next(NULL) {}
};

class LRUCache {
public:
    map<int, Node*> cache;
    Node* lru_head;
    Node* lru_tail;
    int lru_size;
    int lru_capacity;
    LRUCache(int capacity):
        lru_head(NULL),
        lru_tail(NULL),
        lru_size(0),
        lru_capacity(capacity) {
    }
    void put_back(Node* x) {
        if (lru_size == 1) return ;
        if (lru_tail == x) return ;
        if (lru_head == x) {
            lru_head = lru_head -> next;
        } else {
            Node* n = x -> next;
            Node* p = x -> prev;
            p -> next = n;
            n -> prev = p;
        }
        lru_tail -> next = x;
        x -> prev = lru_tail;
        x -> next = NULL;
        lru_tail = x;
    }

    int get(int key) {
        map<int, Node*>::const_iterator it = cache.find(key);
        if (it == cache.end()) {
            return -1;
        }
        Node* x = it -> second;
        put_back(x);
        return x -> value;
    }

    void debug_print() {
        Node* t = lru_head;
        printf("nodes:");
        while(t) {
            printf(" [%d,%d]", t -> key, t -> value);
            t = t -> next;
        }
        printf("\n");
    }

    void clear(int capacity) {
        cache.clear();
        lru_head = NULL;
        lru_tail = NULL;
        lru_size = 0;
        lru_capacity = capacity;
    }

    void set(int key, int value) {
        map<int, Node*>::const_iterator it = cache.find(key);
        Node* n = NULL;
        if (it == cache.end()) {
            if (lru_size == lru_capacity) {
                n = lru_head;
                cache.erase(n -> key);
            } else {
                n = new Node(key, value);
                lru_size ++;
                // put at front temporarily
                if (lru_head == NULL) {
                    lru_tail = n;
                } else {
                    n -> next = lru_head;
                    lru_head -> prev = n;
                }
                lru_head = n;
            }
            cache[key] = n;
        } else {
            n = it -> second;
        }
        put_back(n);
        n -> key = key;
        n -> value = value;
    }
};

int main() {
    LRUCache c(3);
    c.set(1, 1);
    c.set(2, 2);
    c.set(3, 3);
    c.set(4, 4);
    c.debug_print();
    c.set(5, 5);
    c.debug_print();
    assert(c.get(3) == 3);
    c.set(6, 6);
    c.debug_print();

    c.clear(2);
    c.set(2, 1);
    c.set(1, 1);
    c.set(2, 3);
    c.set(4, 1);
    c.debug_print();
    return 0;
}
