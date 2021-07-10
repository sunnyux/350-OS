#!/usr/bin/env python3
import subprocess
import sys
import re

expected = "OS/161 kernel: p uw-testbin/onefork\nP\nC\nOperation took"
expected1 = "OS/161 kernel: p uw-testbin/onefork\nPC\n\nOperation took"

shutting_down = "The system is halted."


test = "p uw-testbin/onefork;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if (expected in output or expected1 in output) and shutting_down in output and "panic" not in output:
        print(str(r))
    else:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)

print(output)
print("Done all tests on " + test)

