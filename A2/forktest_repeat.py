#!/usr/bin/env python3
import subprocess
import sys
import re

expected = re.compile("OS/161 kernel [? for menu]: p testbin/forktest\n(program name unknown): Starting.\n0+1+2+3+\n(program name unknown): Complete.\nOS/161 kernel: q\nShutting down.\nThe system is halted.")

# test = 'p uw-testbin/widefork;q'
test = "p testbin/forktest;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if expected.match(output) and "panic" not in output:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
    else: 
        print(str(r))

print("Done all tests on " + test)

