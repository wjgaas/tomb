#include <string>
#include <algorithm>
#include <cstdio>
using namespace std;

class Solution {
public:
    void reverseWords(string& s) {
        int size = s.size();
        // trim and merge continual spaces.
        int f = 0, l = size - 1;
        while(f < size && s[f] == ' ') f++;
        while(l >= 0 && s[l] == ' ') l--;
        if(f > l) {
            s = "";
            return ;
        } else {
            string tmp("");
            for(int i = f; i <= l; i++) {
                if(s[i] == ' ' && s[i - 1] == ' ') {
                    // ignore.
                    continue;
                }
                tmp += s[i];
            }
            s = tmp;
        }
        int last = 0;
        size = s.size();
        for(int i = 0; i < size; i++) {
            if(s[i] == ' ') {
                reverse(s.begin() + last, s.begin() + i);
                last = i + 1;
            }
        }
        reverse(s.begin() + last, s.end());
        reverse(s.begin(), s.end());
    }
};

int main() {
    Solution s;
    {
        string str("the sky is blue");
        s.reverseWords(str);
        printf("%s\n", str.c_str());
    }
    {
        string str("  ");
        s.reverseWords(str);
        printf("%s\n", str.c_str());
    }
    {
        string str("   a   b ");
        s.reverseWords(str);
        printf("%s\n", str.c_str());
    }
    {
        string str("hi!");
        s.reverseWords(str);
        printf("%s\n", str.c_str());
    }
    return 0;
}
