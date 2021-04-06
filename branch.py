#!/usr/bin/env python3

# see x86_64 instruction set
cond_branch_ops = [
  'ja', 'jae', 'jb', 'jbe', 'jc',
  'jecxz', 'jrcxz',
  'je', 'jg', 'jge', 'jl', 'jle',
  'jna', 'jnae', 'jnb', 'jnbe',
  'jnc', 'jne', 'jng', 'jnge', 'jnl', 'jnle',
  'jno', 'jnp', 'jns', 'jnz',
  'jo', 'jp', 'jpe', 'jpo', 'js', 'jz'
]


class Branch:
  def __init__(self, op, addr, target):
    self._op = op
    self._addr = addr
    self._target = target
    # branch stats
    self._count = 0
    self.t = 0
    self.nt = 0
    self._order = []

  @property
  def op(self):
    return self._op

  @op.setter
  def op(self, op):
    assert op in cond_branch_ops
    self._op = op

  @property
  def addr(self):
    return self._addr

  @addr.setter
  def addr(self, addr):
    assert addr >= 0
    self._addr = addr

  @property
  def target(self):
    return self._target

  @target.setter
  def target(self, target):
    assert target >= 0
    self._target = target

  def count(self):
    return self._count

  def order(self):
    return self._order

  def taken(self):
    return self.t

  def not_taken(self):
    return self.nt

  def take(self):
    self._count += 1
    self.t += 1
    self._order.append(True)

  def notake(self):
    self._count += 1
    self.nt += 1
    self._order.append(False)

  def plot(self):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tk

    fig, ax = plt.subplots()
    ax.plot(range(self._count), self._order, '.', color='red')
    ax.set_xlabel('Num Executions')
    ax.set_ylabel('TNT')
    ax.title.set_text(self.op + ' 0x' + str(self._addr))
    ax.yaxis.set_major_locator(tk.FixedLocator([0, 1]))
    ax.set_yticklabels(['NT', 'T'])
    ax.set_ylim(-0.1, 1.1)
    fig.savefig(self.op + '-0x' + str(self._addr) + '.png')

  def __repr__(self):
    return 'Branch [op: ' + self._op + ', addr: ' + hex(self._addr) + \
           ', target: ' + hex(self._target) + \
           ', count: ' + str(self._count) + \
           ', taken: ' + str(self.t) + \
           ', not taken: ' + str(self.nt) + \
           ', order: ' + str(self._order) + ']'

  def __str__(self):
    return 'Branch [op: ' + self._op + ', addr: ' + hex(self._addr) + \
           ', target: ' + hex(self._target) + \
           ', count: ' + str(self._count) + \
           ', taken: ' + str(self.t) + \
           ', not taken: ' + str(self.nt) + \
           ', order: ' + str(self._order) + ']'


class BranchInfo:
  def __init__(self, branches):
    self._start = -1
    self._stop = -1
    self._branches = branches

  def branch(self, addr):
    return self._branches.get(addr)

  def branches(self):
    return self._branches.values()

  @property
  def start(self):
    return self._start

  @start.setter
  def start(self, time):
    self._start = time

  @property
  def stop(self):
    return self._stop

  @stop.setter
  def stop(self, time):
    self._stop = time

  def __repr__(self):
    ret = 'BranchInfo [start: ' + str(self._start) 
    ret += ', stop: '+  str(self._stop)
    ret += ', branches:\n'
    for a in self.branches:
      ret += '\t' + str(self.branches[a]) + '\n'
    ret += ']'
    return ret


def search_binary(binary):
  import os
  import re

  print('Warning: executable must be compiled with \'-no-pie\' enabled, ' + \
        'otherwise branch info will (probably) be wrong')
  objdump = 'objdump -d ' + binary
  print("Searching for branch instructions from \'" + objdump + "\'...")
  asm_dump = os.popen(objdump)
  branches = {}
  for line in asm_dump:
    # FIXME: hard code line length is kinda dumb
    if len(line) < 32 or not re.match(r'\s*[0-9a-f]+:', line):
      continue
    # addr: hex    opcode operand
    sec = line.split()
    addr = int(sec[0][:-1], 16)
    ops = line[32:-1].split()           # FIXME: hard code line len
    op = ops[0]
    if op in cond_branch_ops:
      target = int(ops[1], 16) # target address
      branches[addr] = Branch(op, addr, target)
  asm_dump.close()
  print("Found %d conditional branches" % len(branches))
  return branches

