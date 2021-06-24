#!/usr/bin/env python3
import subprocess
import sys
import string
import random

expected = "TEST SUCCEEDED"
for r in range(1000):
	output = subprocess.run(['sys161 kernel-ASST2 "uw1;q"'], capture_output=True, text=True).stdout
	t = output.splitlines()[0]
	if t not in expected:
		sys.exit(output)
	else: 
		print(str(r))

