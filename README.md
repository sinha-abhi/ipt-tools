iptba
=====

Analyze branch behavior using Intel PT.

Commands
--------

get perf.data using perf-intel-pt: `perf record -e intel_pt//u <command>`

use iptba: `perf script --itrace=i1ns -s iptba/iptba-script.py <command>`

run all tests: `python3 -m unittest --verbose`

run specific test: `python3 -m unittest --verbose test.test_<name>`

TODO
----
- [ ] plot behavior of "interesting" branches
  - [ ] collect data from SPEC cpu2017 benchmark suite
