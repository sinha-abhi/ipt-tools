import atexit
import os
import subprocess as sp
import unittest

from iptba.branch import Branch

from test.programs import *


wd = os.getcwd()

def helper_test_programs(test_file):
  print('testing %r' % test_file)
  _tf = 'test/' + test_file
  st = os.path.join(wd, _tf + '.c')
  if not os.path.isfile(st):
    with open(st, 'x') as _st:
      _st.write(simple_test)
  sp.run('gcc -o ' + _tf + ' ' + _tf + '.c', shell=True, check=True)
  return os.popen('objdump -d ' + _tf)


class TestBranch(unittest.TestCase):
  def test_simple_dump(self):
    dump = helper_test_programs('simple-test')
    branches = Branch.process_asm_dump(dump)
    dump.close()
    self.assertEqual(len(branches), 3)

