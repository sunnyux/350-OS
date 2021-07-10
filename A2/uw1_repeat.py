#!/usr/bin/env python3
import subprocess
import sys
import string
import random

expected = "TEST SUCCEEDED"
shutting_down = "The system is halted."


for r in range(2000):
	output = subprocess.run(['sys161', 'kernel-ASST2', 'uw1;q'], capture_output=True, text=True).stdout
	if expected in output and shutting_down in output and "panic" not in output:
		print(str(r))
	else:
		p = output + "\n" + "FAILED"
		sys.exit(p)

print(output)
print("Done all tests")
