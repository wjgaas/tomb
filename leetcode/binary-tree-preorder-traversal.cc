/**
 * Definition for binary tree
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */

#include <vector>
#include <cstdio>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> v;
        act(root, v);
        return v;
    }
    void act(TreeNode* root, vector<int>& v) {
        if (root == NULL) return ;
        v.push_back(root -> val);
        act(root -> left, v);
        act(root -> right, v);
    }
};

int main() {
    return 0;
}
