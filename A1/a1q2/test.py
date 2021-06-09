#!/usr/bin/env python3
import subprocess
import sys



for c in range(6, 20):
	for p in range(10):
		for r in range(20):
			if c <= p * r and c > 0 and p > 0 and r > 0:
				stderr = subprocess.run(['./a1q2', str(c), str(p), str(r)], capture_output=True, text=True).stderr
				if "failed" in stderr:
					print(stderr)
					string = "Assertion failed, ./a1q2 " + str(c) + " " + str(p) + " " + str(r)
					sys.exit(string)
				else: 
					print(str(c) + " " + str(p) + " " + str(r))

