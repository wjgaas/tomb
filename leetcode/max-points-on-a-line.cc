/**
 * Definition for a point.
 * struct Point {
 *     int x;
 *     int y;
 *     Point() : x(0), y(0) {}
 *     Point(int a, int b) : x(a), y(b) {}
 * };
 */

#include <vector>
using namespace std;

struct Point {
    int x;
    int y;
    Point() : x(0), y(0) {}
    Point(int a, int b) : x(a), y(b) {}
};
class Solution {
public:
    int maxPoints(vector<Point>& points) {
        vector<Point> nps;
        vector<int> cnts;

        // better merge points.
        int n = points.size();
        if (n == 0) return n;
        for(int i = 0; i < n; i++) {
            int seen = -1;
            for(int j = 0; j < nps.size(); j++) {
                int dy = (points[i].y - nps[j].y);
                int dx = (points[i].x - nps[j].x);
                if (dx == 0 && dy == 0) {
                    seen = j;
                    break;
                }
            }
            if(seen == -1) {
                nps.push_back(points[i]);
                cnts.push_back(1);
            } else {
                cnts[seen] += 1;
            }
        }

        // iteration.
        n = nps.size();
        if (n == 1) return cnts[0];
        int ret = 0;
        for (int i = 0; i < n; i++) {
            for(int j = i + 1; j < n; j++) {
                int dy = nps[i].y - nps[j].y;
                int dx = nps[i].x - nps[j].x;
                int sum = cnts[i] + cnts[j];
                for(int k = j + 1; k < n; k++) {
                    int dky = (nps[k].y - nps[j].y);
                    int dkx = (nps[k].x - nps[j].x);
                    if (dky * dx == dkx * dy) {
                        sum += cnts[k];
                    }
                }
                if (sum > ret) ret = sum;
            }
        }
        return ret;
    }
};

int main() {
    return 0;
}
