#include <string>
#include <stack>
#include <vector>
#include <cstdlib>
using namespace std;

#define POP2                                  \
  int a = si.top();                           \
  si.pop();                                   \
  int b = si.top();                           \
  si.pop()

class Solution {
public:
  int evalRPN(vector<string> &tokens) {
    stack<int> si;
    for(int i = 0; i < tokens.size(); i++) {
      const string& s = tokens[i];
      if(s == "+") {
        POP2;
        si.push(a + b);
      } else if(s == "-") {
        POP2;
        si.push(b - a);
      } else if(s == "*") {
        POP2;
        si.push(a * b);
      } else if(s == "/") {
        POP2;
        si.push(b / a);
      } else {
        int v = atoi(s.c_str());
        si.push(v);
      }
    }
    return si.top();
  }
};

int main() {
  return 0;
}
