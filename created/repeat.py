#!/usr/bin/env python3
import subprocess
import sys
import string
import random

expected = "Starting lock test...\ncleanitems: Destroying sems, locks, and cvs"
for r in range(1000):
	output = subprocess.run(['sys161 kernel-ASST2 "sy2;q"'], capture_output=True, text=True).stdout
	t = output.splitlines()[0]
	if t not in expected:
		sys.exit(output)
	else: 
		print(str(r))

