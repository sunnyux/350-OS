#!/usr/bin/env python3
import subprocess
import sys
import string
import random

reverse = "Thread 31\nThread 30\nThread 29\nThread 28\nThread 27\nThread 26\nThread 25\nThread 24\nThread 23\nThread 22\nThread 21\nThread 20\nThread 19\nThread 18\nThread 17\nThread 16\nThread 15\nThread 14\nThread 13\nThread 12\nThread 11\nThread 10\nThread 9\nThread 8\nThread 7\nThread 6\nThread 5\nThread 4\nThread 3\nThread 2\nThread 1\nThread 0\n"
expected = reverse * 5

for r in range(2000):
	output = subprocess.run(['sys161', 'kernel-ASST2', 'sy3;q'], capture_output=True, text=True).stdout
	if expected not in output:
		p = output + "\n" + "FAILED"
		sys.exit(p)
	else: 
		print(str(r))

print("Done all tests")

