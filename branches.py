#!/usr/bin/env python3
import re

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
    self._count = 0

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

  def inc(self):
    self._count += 1

  @staticmethod
  def process_asm_dump(asm_dump):
    branches = {}
    for line in asm_dump:
      # FIXME: hard code line length is kinda dumb
      if len(line) < 32 or not re.match(r'\s*[\d\a]+:', line):
        continue
      # addr: hex    opcode operand
      sec = line.split()
      addr = int(sec[0][:-1], 16)
      ops = line[32:-1].split()           # FIXME: hard code line len
      op = ops[0]
      if op in cond_branch_ops:
        target = int(ops[1], 16) # target address
        branches[addr] = Branch(op, addr, target)
    return branches

  def __repr__(self):
    return 'Branch [op: ' + self._op + ', addr: ' + hex(self._addr) + \
      ', target: ' + hex(self._target) + ']'

  def __str__(self):
    return 'Branch [op: ' + self._op + ', addr: ' + hex(self._addr) + \
      ', target: ' + hex(self._target) + ']'


