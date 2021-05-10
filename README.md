ipt-tools
=====

A set of tools to analyze trace data generated from Intel PT.

### iptba

Analyze conditional branch behavior. 

1. Generate `perf.data` with Intel PT enabled
```bash
perf record -e intel_pt//u <command>
```

2. Use `perf script` with provided script
```bash
perf script --itrace=i1ns -s iptba-script.py <command>
```

**NOTE**  Executables need to be compiled with the `-no-pie` flag enabled (in gcc).

### iptdiff -- **WIP**

Compare two trace data of an executable.

### TODO
- [ ] port `iptba` to C/C++
- [ ] prototype of `iptdiff`
