#!/usr/bin/env python3
import subprocess
import sys
import re

starting = "OS/161 kernel: p uw-testbin/hogparty"
expected = re.compile("[xyz]+\n[xyz]+\n[xyz]+")
shutting_down = "The system is halted."

test = "p uw-testbin/hogparty;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if re.search(expected, output) and starting in output and shutting_down in output and "panic" not in output:
        print(str(r))
    else:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)

print(output)
print("Done all tests on " + test)

