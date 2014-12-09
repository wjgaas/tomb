#include <cstdio>
#include <cstring>
#include <cassert>
#include <algorithm>
#include <set>
#include <queue>

class Solution {
public:
    int jump(int A[], int n) {
        std::set<int> idxs;
        typedef std::pair<int, int> IntPair;
        typedef std::set<int>::const_iterator SetIterator;
        std::queue< IntPair > Q;

        // we already at idx#0.
        for(int i = 1; i < n; i++) idxs.insert(i);
        Q.push(IntPair(0, 0));
        while (!Q.empty()) {
            IntPair p = Q.front();
            Q.pop();
            if (p.first == (n - 1)) return p.second;
            int v = A[p.first];
            SetIterator beg = idxs.upper_bound(p.first);
            std::vector<int> pts; // for remove.
            for(SetIterator it = beg; it != idxs.end() && *it <= (p.first + v); ++it) {
                Q.push(IntPair(*it, p.second + 1));
                pts.push_back(*it);
            }
            for(int i = 0; i < pts.size(); i++) {
                idxs.erase(pts[i]);
            }
        }
    }
};

int main() {
    Solution s;
    int A[] = {2, 1, 1, 1, 1};
    // int A[] = {1, 2};
    // int A[] = {2,3,1,1,4};
    // int A[] = {9,8,2,2,0,2,2,0,4,1,5,7,9,6,6,0,6,5,0,5};
    // int A[25000];
    // for (int i=0;i<25000;i++) A[i] = 25000-i-2;
    int size = sizeof(A) / sizeof(A[0]);
    printf("%d\n", s.jump(A, size));
    return 0;
}
