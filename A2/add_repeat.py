#!/usr/bin/env python3
import subprocess
import sys
import re

shutting_down = "Shutting down.\nThe system is halted."

for i in range(100, 200):
    for j in range(5100, 5300):
        command  = "p testbin/add " + str(i) + " " + str(j)
        expected = command + "\nAnswer: " + str(i+j) + "\nOperation took"
        test     = command + ";q"
    
        output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
        if expected in output and shutting_down in output and "panic" not in output:
            print(str(i) + " " + str(j))
        else:
            # if expected not in output:
            p = output + "\n" + "FAILED"
            sys.exit(p)
            
        
print(output)
print("Done all tests on " + test)

