#include <cstdio>
#include <string>
using namespace std;

class Solution {
public:
    string convert(string s, int nRows) {
        string res;
        size_t sz = s.size();
        if (sz <= nRows) return s;
        for (int r = 0; r < nRows; r++) {
            int idx = r;
            res += s[idx];
            while (idx < sz) {
                idx += 2 * (nRows - 1);
                if (!(r == 0 || r == (nRows - 1))) {
                    if ((idx - 2 * r) < sz) res += s[idx - 2 * r];
                }
                if (idx < sz) res += s[idx];
            }
        }
        return res;
    }
};

int main() {
    Solution sn;
    string s = "PAYPALISHIRING";
    string res = sn.convert(s, 3);
    printf("%s\n", res.c_str());
    return 0;
}
