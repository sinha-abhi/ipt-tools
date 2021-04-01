#!/usr/bin/env python3

# Analyze branch behavior using perf-intel-pt

from __future__ import print_function

import os
import sys

sys.path.append(os.environ['PERF_EXEC_PATH'] + \
  '/scripts/python/Perf-Trace-Util/lib/Perf/Trace')

from perf_trace_context import *
from Core import *

from branch import Branch, BranchInfo, search_binary


def trace_begin():
  if len(sys.argv) < 2:
    print('Usage: perf script --itrace=i1ns -s iptba.py <command>')
    exit(0)


branches = search_binary(sys.argv[1])
binfo = BranchInfo(branches)
prev_branch_addr = 0

def process_event(params_dict):
  global prev_branch_addr
  global ic
  sample = params_dict['sample']
  addr = sample['ip']
  t = sample['time']
  binfo.stop = t
  if binfo.start == -1:
    binfo.start = t
  if prev_branch_addr != 0:
    branch = binfo.branch(prev_branch_addr)
    if addr == branch.target:
      branch.take()
    else:
      branch.notake()
  if binfo.branch(addr) != None:
    prev_branch_addr = addr
  else:
    prev_branch_addr = 0


def trace_end():
  print('Done processing trace')
  print(binfo)

