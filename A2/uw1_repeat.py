#!/usr/bin/env python3
import subprocess
import sys
import string
import random

expected = "TEST SUCCEEDED"

for r in range(2000):
	output = subprocess.run(['sys161', 'kernel-ASST2', 'uw1;q'], capture_output=True, text=True).stdout
	if expected not in output:
		p = output + "\n" + "FAILED"
		sys.exit(p)
	else: 
		print(str(r))

print("Done all tests")
