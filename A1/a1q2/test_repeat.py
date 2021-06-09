#!/usr/bin/env python3
import subprocess
import sys



for i in range(300):
	stdout = subprocess.run(['./a1q2_for_loop', '3', '2', '6'], capture_output=True, text=True).stdout
	stderr = subprocess.run(['./a1q2_for_loop', '3', '2', '6'], capture_output=True, text=True).stderr
	if "failed" in stderr:
		print(stderr)
		print(stdout)
		string = "Assertion failed, ./a1q2_for_loop 3 2 6"
		sys.exit(string)
	else:
		print(i)