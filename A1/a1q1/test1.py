#!/usr/bin/env python3
import subprocess
import sys
import string
import random

letters = string.ascii_lowercase

for r in range(1000):
	c = random.choice(letters) + random.choice(letters) + random.choice(letters)
	threaded = subprocess.run(['./a1q1', str(r), c], capture_output=True, text=True).stdout
	none_threaded = subprocess.run(['./a1q1_non_threaded', str(r), c], capture_output=True, text=True).stdout
	t = threaded.splitlines()[0]
	n = none_threaded.splitlines()[0]
	if t != n:
		string = "Count mismatching: ./a1q1" + str(r) + " " + c + "\n" + "Threaded: " + t + ", Non-threaded: " + n
		sys.exit(string)
	else: 
		print(str(r) + " " + c + " " + t + " " + n)