#include <cstdio>
#include <cstring>
#include <cassert>
#include <algorithm>
#include <set>
#include <queue>

class Solution {
public:
    bool canJump(int A[], int n) {
        std::set<int> idxs;
        typedef std::pair<int, int> IntPair;
        typedef std::set<int>::const_iterator SetIterator;
        std::queue< IntPair > Q;

        if (n == 0) return false;
        // we already at idx#0.
        for(int i = 1; i < n; i++) idxs.insert(i);
        Q.push(IntPair(0, 0));
        while (!Q.empty()) {
            IntPair p = Q.front();
            Q.pop();
            if (p.first == (n - 1)) return true;
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
        return false;
    }
};

int main() {
    return 0;
}
