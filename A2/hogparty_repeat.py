#!/usr/bin/env python3
import subprocess
import sys
import re

expected = re.compile("OS/161 kernel [? for menu]: p uw-testbin/hogparty\n[xyz]+\n[xyz]+\n[xyz]+\nOperation took")
# expected = "OS/161 kernel: p uw-testbin/pidcheck\nC: 2\nPC: 2\nPP: 1\nOperation took"
# expected = "OS/161 kernel: p uw-testbin/widefork\nP\nP\nA\nB\nP\nC\nOperation took"
# expected = re.compile("(program name unknown): Starting.\n0+1+2+3+\n(program name unknown): Complete.")

test = "p uw-testbin/hogparty;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if expected.match(output) and "panic" not in output:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
    else: 
        print(str(r))
print(output)
print("Done all tests on " + test)

