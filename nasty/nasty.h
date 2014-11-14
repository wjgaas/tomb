/* coding:utf-8
 * Copyright (C) dirlt
 */

#ifndef __CC_NASTY_NASTY_H__
#define __CC_NASTY_NASTY_H__

#include <string>
#include <vector>
#include <ostream>

namespace nasty {

class Expr;
class Atom;

class Parser {
public:
    Parser(const char* f) :
        f_(f), ex_(0) {}
    const std::string& file() const {
        return f_;
    }
    Expr* run();
    Expr* run(FILE* fin);
    Expr* run(std::string s);
    void setExpr(Expr* ex) {
        ex_ = ex;
    }
    ~Parser();
private:
    std::string f_; // filename
    Expr* ex_;
}; // class Parser

class Expr {
public:
    enum Type {
        STR,  // string
        ID,    // identifier
        FLT,   // float number
        INT,   // integer number
        TREE,  // tree holds expressions
    };
    Expr(Type type, const char* text,
         int leng, int line, int column):
        type_(type), text_(text, leng),
        line_(line), column_(column) {}
    Expr(): type_(TREE) {}
    const std::vector< Expr* >& tree() const {
        return tree_;
    }
    void appendExpr(Expr* ex);
    ~Expr();
    std::string toString() const ;
private:
    friend class Parser;
    void write(std::ostream& os) const;
    Type type_;
    std::string text_;
    int line_;
    int column_;
    std::vector< Expr* > tree_;
}; // class Expr

} // namespace nasty

#endif // __CC_NASTY_NASTY_H__
