#include <algorithm>
#include <array>
#include <cstdio>
#include <iostream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "branch.h"

std::vector<std::string> cond_branch_ops {
  "ja", "jae", "jb", "jbe", "jc",
  "jecxz", "jrcxz",
  "je", "jg", "jge", "jl", "jle",
  "jna", "jnae", "jnb", "jnbe",
  "jnc", "jne", "jng", "jnge", "jnl", "jnle",
  "jno", "jnp", "jns", "jnz",
  "jo", "jp", "jpe", "jpo", "js", "jz"
};

std::ostream &operator<<(std::ostream &o, const Branch &b) {
  o << "[op: " << b.op; 
  o << ", addr: " << std::hex << b.addr;
  o << ", target: " << b.target;
  o << std::dec << ", count: " << b.get_count();
  o << ", taken: " << b.tc << ", not taken: " << b.ntc;
  o << ", order: (";
  if (b.order.empty()) {
    o << ")";
  } else {
    for (unsigned i = 0; i < b.order.size(); ++i)
      o << b << " )"[i == b.order.size()];
  }
  o << "]";

  return o;
}

std::map<unsigned, Branch> objdump_decode(std::string bf) {
  std::map<unsigned, Branch> branches;

  std::array<char, 256> buf;
  std::string cmd = "objdump -d " + bf;
  std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
  if (!pipe)
    throw std::runtime_error("popen failed");

  std::string line, op;
  unsigned addr, target;
  std::vector<std::string> secs, op_secs;
  std::vector<std::string>::iterator it;
  std::regex re("^\\s*[0-9a-f]+:");
  while (fgets(buf.data(), buf.size(), pipe.get())) {
    line = buf.data();
    if ((line.length() < 32) || !(std::regex_search(line, re)))
      continue;
    std::istringstream line_ss(line);
    std::copy(std::istream_iterator<std::string>(line_ss),
              std::istream_iterator<std::string>(),
              back_inserter(secs));

    secs.at(0).pop_back();
    addr = (unsigned) strtoul(secs.at(0).c_str(), NULL, 16);
    std::istringstream op_ss(line.substr(32));
    std::copy(std::istream_iterator<std::string>(op_ss),
              std::istream_iterator<std::string>(),
              back_inserter(op_secs));
    op = op_secs.at(0);
    it = std::find(cond_branch_ops.begin(), cond_branch_ops.end(), op);
    if (it != cond_branch_ops.end()) {
      target = (unsigned) strtoul(op_secs.at(1).c_str(), NULL, 16);
      branches.insert(std::make_pair(addr, Branch(op, addr, target)));
    }

    secs.clear();
    op_secs.clear();
  }

  return branches;
}

int main() {
  std::string exe = "test/a.out";
  auto branches = objdump_decode(exe);
  for (auto &b : branches)
    std::cout << b.first << " " << b.second << std::endl;

  return 0;
}
