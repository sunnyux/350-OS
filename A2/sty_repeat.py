#!/usr/bin/env python3
import subprocess
import sys
import re

expected = "OS/161 kernel: p testbin/sty\nOperation took "
shutting_down = "Shutting down.\nThe system is halted."


test = "p testbin/sty;q"

for r in range(2000):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if expected in output and shutting_down in output and "panic" not in output:
        print(str(r))
    else:
        # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
        
print(output)
print("Done all tests on " + test)

