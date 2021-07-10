#!/usr/bin/env python3
import subprocess
import sys
import string
import random

reverse = "sy2\nStarting lock test...\ncleanitems: Destroying sems, locks, and cvs\nLock test done.\nOperation took"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', 'sy2;q'], capture_output=True, text=True).stdout
    if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
    else: 
        print(str(r))

print(output)
print("Done all tests")

