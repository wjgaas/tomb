/* coding:utf-8
 * Copyright (C) dirlt
 */

#include <iostream>
#include <vector>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
using namespace std;
using namespace boost::python;

class Item {
  public:
    int x;
    int y;
    Item(int x, int y = 10): x(x), y(y) {}
    void echo(const string& arg = "world") {
        cerr << arg << endl;
    }
    bool operator==(const Item& other) const {
        return other.x == x && other.y == y;
    }
};
int add(int x, int y) {
    return x + y;
}
using ItemArray = std::vector<Item>;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(Item_overloads, echo, 0, 1);
BOOST_PYTHON_MODULE(test_pye)
{
    class_<Item>("Item",
                 init<int, optional<int>>((args("x"), args("y") = 10)))
            .def_readwrite("x", &Item::x)
            .def_readwrite("y", &Item::y)
            .def("echo", &Item::echo, Item_overloads())
            ;
    def("add", add);
    class_<ItemArray>("ItemArray")
            .def(vector_indexing_suite<ItemArray>());
}
