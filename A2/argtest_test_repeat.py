#!/usr/bin/env python3
import subprocess
import sys
import re

starting = "p uw-testbin/argtest test\nargc   : 2"
expected = "argv[0] -> uw-testbin/argtest\nargv[1] -> test\nargv[2] -> [NULL]\nOperation took"
shutting_down = "Shutting down.\nThe system is halted."


test = "p uw-testbin/argtest test;q"

for r in range(10):
    output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
    if starting in output and expected in output and shutting_down in output and "panic" not in output:
        print(str(r))
    else:
    # if expected not in output:
        p = output + "\n" + "FAILED"
        sys.exit(p)
        
print(output)
print("Done all tests on " + test)

