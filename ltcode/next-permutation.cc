#include <vector>
#include <algorithm>
#include <functional>
using namespace std;

class Solution {
public:
    void nextPermutation(vector<int>& num) {
        int size = num.size();
        for(int i = size - 1; i >= 0; i--) {
            int j = size - 1;
            int choose = -1;
            while(j > i) {
                if (num[j] > num[i]) {
                    if (choose == -1 ||
                            num[j] < num[choose]) {
                        choose = j;
                    }
                }
                j--;
            }
            if(choose != -1) {
                swap(num[i], num[choose]);
                sort(num.begin() + i + 1,
                     num.end());
                return ;
            }
        }
        // then reverse all
        reverse(num.begin(), num.end());
    }
};

int main() {
    return 0;
}
