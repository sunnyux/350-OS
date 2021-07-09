#!/usr/bin/env python3
import subprocess
import sys
import re

starting = "OS/161 kernel: p testbin/forktest\ntestbin/forktest: Starting."
expected = re.compile("0*1*2*3*")
complete = "testbin/forktest: Complete.\nOperation took"
shutting_down = "Shutting down.\nThe system is halted."

test = "p testbin/forktest;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if starting in output and re.search(expected, output) and complete in output and shutting_down in output and "panic" not in output:
        print(str(r))
    else:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
        
print(output)
print("Done all tests on " + test)

