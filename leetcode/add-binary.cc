#include <cstdio>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    string addBinary(string a, string b) {
        int f = 0;
        int ap = a.size() - 1;
        int bp = b.size() - 1;
        string s = "";
        while(ap >= 0 && bp >= 0) {
            f += a[ap] - '0' + b[bp] - '0';
            s += (f & 0x1) + '0';
            f >>= 1;
            ap--;
            bp--;
        }
        while(ap >= 0) {
            f += a[ap] - '0';
            s += (f & 0x1) + '0';
            f >>= 1;
            ap--;
        }
        while(bp >= 0) {
            f += b[bp] - '0';
            s += (f & 0x1) + '0';
            f >>= 1;
            bp--;
        }
        if (f) s += '1';
        reverse(s.begin(), s.end());
        return s;
    }
};

int main() {
    Solution s;
    string r = s.addBinary("11", "1");
    printf("%s\n", r.c_str());
    return 0;
}
