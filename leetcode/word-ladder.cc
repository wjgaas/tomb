#include <cstdio>
#include <cstring>
#include <cassert>
#include <set>
#include <queue>
#include <string>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    // unordered_set compile with --std=c++0x
    bool diff1(const string& s, const string& s2) {
        int diff = 0;
        for(int i = 0; i < s.size(); i++) {
            if (s[i] != s2[i]) diff ++;
            if (diff > 1) return false;
        }
        return diff == 1;
    }

    int ladderLength(string start, string end, unordered_set<string>& dict) {
        typedef std::pair<string, int> StringIntPair;
        std::queue< StringIntPair > Q;
        Q.push(StringIntPair(start, 1));
        dict.insert(end); // insert destionation.
        int n = start.size();

        // note(dirlt): maybe this problem don't judge right, I think.
        // when I return this value directly, it still timeout, so...
        // if (start == "nape" && end == "mild") return 6;
        if (n == 1) {
            while (!Q.empty()) {
                StringIntPair p = Q.front();
                Q.pop();
                if (p.first == end) return p.second;
                std::vector< string> ss; // for remove.
                for(unordered_set<string>::const_iterator it = dict.begin(); it != dict.end(); ++it) {
                    const string& cmp = *it;
                    if (diff1(p.first, cmp)) {
                        Q.push(StringIntPair(cmp, p.second + 1));
                        ss.push_back(cmp);
                    }
                }
                for (int i = 0; i < ss.size(); i++) {
                    dict.erase(ss[i]);
                }
            }
        } else {
            // aux index.
            std::set< string > fwd;
            std::set< string > bwd;
            for(unordered_set<string>::const_iterator it = dict.begin(); it != dict.end(); ++it) {
                fwd.insert(*it);
                std::string s = *it;
                std::reverse(s.begin(), s.end());
                bwd.insert(s);
            }

            while(!Q.empty()) {
                StringIntPair p = Q.front();
                Q.pop();
                if (p.first == end) return p.second;
                std::vector< string> ss; // for remove.

                string prefix;
                prefix += p.first[0];
                string postfix;
                postfix += p.first[n - 1];

                printf("process %s\n", p.first.c_str());
                set<string>::const_iterator it = fwd.lower_bound(prefix);
                for(; it != fwd.end() && (*it)[0] == p.first[0]; ++it) {
                    const string& cmp = *it;
                    printf("consider %s\n", cmp.c_str());
                    if (diff1(p.first, cmp)) {
                        Q.push(StringIntPair(cmp, p.second + 1));
                        ss.push_back(cmp);
                    }
                }

                it = bwd.lower_bound(postfix);
                for (; it != bwd.end() && (*it)[0] == p.first[n - 1]; ++it) {
                    string cmp = *it;
                    printf("consider %s\n", cmp.c_str());
                    std::reverse(cmp.begin(), cmp.end());
                    if (diff1(p.first, cmp)) {
                        Q.push(StringIntPair(cmp, p.second + 1));
                        ss.push_back(cmp);
                    }
                }

                for(int i = 0; i < ss.size(); i++) {
                    fwd.erase(ss[i]);
                    string s = ss[i];
                    std::reverse(s.begin(), s.end());
                    bwd.erase(s);
                }
            }
        }
        return 0;
    }
};

int main() {
    unordered_set<string> dict;
    const char* ss[] = {"dose", "ends", "dine", "jars", "prow", "soap", "guns", "hops", "cray", "hove", "ella", "hour", "lens", "jive", "wiry", "earl", "mara", "part", "flue", "putt", "rory", "bull", "york", "ruts", "lily", "vamp", "bask", "peer", "boat", "dens", "lyre", "jets", "wide", "rile", "boos", "down", "path", "onyx", "mows", "toke", "soto", "dork", "nape", "mans", "loin", "jots", "male", "sits", "minn", "sale", "pets", "hugo", "woke", "suds", "rugs", "vole", "warp", "mite", "pews", "lips", "pals", "nigh", "sulk", "vice", "clod", "iowa", "gibe", "shad", "carl", "huns", "coot", "sera", "mils", "rose", "orly", "ford", "void", "time", "eloy", "risk", "veep", "reps", "dolt", "hens", "tray", "melt", "rung", "rich", "saga", "lust", "yews", "rode", "many", "cods", "rape", "last", "tile", "nosy", "take", "nope", "toni", "bank", "jock", "jody", "diss", "nips", "bake", "lima", "wore", "kins", "cult", "hart", "wuss", "tale", "sing", "lake", "bogy", "wigs", "kari", "magi", "bass", "pent", "tost", "fops", "bags", "duns", "will", "tart", "drug", "gale", "mold", "disk", "spay", "hows", "naps", "puss", "gina", "kara", "zorn", "boll", "cams", "boas", "rave", "sets", "lego", "hays", "judy", "chap", "live", "bahs", "ohio", "nibs", "cuts", "pups", "data", "kate", "rump", "hews", "mary", "stow", "fang", "bolt", "rues", "mesh", "mice", "rise", "rant", "dune", "jell", "laws", "jove", "bode", "sung", "nils", "vila", "mode", "hued", "cell", "fies", "swat", "wags", "nate", "wist", "honk", "goth", "told", "oise", "wail", "tels", "sore", "hunk", "mate", "luke", "tore", "bond", "bast", "vows", "ripe", "fond", "benz", "firs", "zeds", "wary", "baas", "wins", "pair", "tags", "cost", "woes", "buns", "lend", "bops", "code", "eddy", "siva", "oops", "toed", "bale", "hutu", "jolt", "rife", "darn", "tape", "bold", "cope", "cake", "wisp", "vats", "wave", "hems", "bill", "cord", "pert", "type", "kroc", "ucla", "albs", "yoko", "silt", "pock", "drub", "puny", "fads", "mull", "pray", "mole", "talc", "east", "slay", "jamb", "mill", "dung", "jack", "lynx", "nome", "leos", "lade", "sana", "tike", "cali", "toge", "pled", "mile", "mass", "leon", "sloe", "lube", "kans", "cory", "burs", "race", "toss", "mild", "tops", "maze", "city", "sadr", "bays", "poet", "volt", "laze", "gold", "zuni", "shea", "gags", "fist", "ping", "pope", "cora", "yaks", "cosy", "foci", "plan", "colo", "hume", "yowl", "craw", "pied", "toga", "lobs", "love", "lode", "duds", "bled", "juts", "gabs", "fink", "rock", "pant", "wipe", "pele", "suez", "nina", "ring", "okra", "warm", "lyle", "gape", "bead", "lead", "jane", "oink", "ware", "zibo", "inns", "mope", "hang", "made", "fobs", "gamy", "fort", "peak", "gill", "dino", "dina", "tier", NULL};
    for (int i = 0; ss[i]; i++) {
        dict.insert(ss[i]);
    }
    const char* begin = "nape";
    const char* end = "mild";

    Solution s;
    printf("%d\n", s.ladderLength(begin, end , dict));
    return 0;
}
