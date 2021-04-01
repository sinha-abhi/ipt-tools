iptba
=====

Analyze branch behavior using Intel PT.

Commands
--------
Note that executables need to be compiled with the `-no-pie` flag enabled.

get perf.data using perf-intel-pt: `perf record -e intel_pt//u <command>`

use iptba: `perf script --itrace=i1ns -s iptba-script.py <command>`

TODO
----
- [ ] plot behavior of "interesting" branches
  - [ ] collect data from SPEC cpu2017 benchmark suite
