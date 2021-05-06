#ifndef _BRANCH_H_
#define _BRANCH_H_

#include <map>
#include <vector>

class Branch {
public:
  Branch(std::string op, unsigned addr, unsigned target) 
    : op(op), addr(addr), target(target), tc(0), ntc(0) { /* empty */ }

  std::string get_op() const           { return op; }
  unsigned get_count() const           { return tc+ntc; }
  unsigned get_taken_count() const     { return tc; }
  unsigned get_not_taken_count() const { return ntc; }
  std::vector<bool> tntorder() const   { return order; }

  void taken() {
    tc++;
    order.push_back(true);
  }

  void not_taken() {
    ntc++;
    order.push_back(false);
  }

  friend std::map<unsigned, Branch> objdump_decode(std::string bf);
  friend std::ostream &operator<<(std::ostream &o, const Branch &b);
private:
  std::string op;
  unsigned addr, target;
  unsigned tc, ntc;
  std::vector<bool> order;
};

#endif /* _BRANCH_H_ */
