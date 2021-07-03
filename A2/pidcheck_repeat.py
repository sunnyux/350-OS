#!/usr/bin/env python3
import subprocess
import sys
import re

# expected = "OS/161 kernel: p uw-testbin/onefork\nP\nC"
# expected = "OS/161 kernel: p uw-testbin/pidcheck\nC: 2\nPC: 2\nPP: 1\nOperation took"
# expected = "OS/161 kernel: p uw-testbin/widefork\nP\nP\nA\nB\nP\nC\nOperation took"
expected = re.compile("OS/161 kernel: p uw-testbin/pidcheck\nC: 2\nPC: 2\nPP: 1\nOperation took*OS/161 kernel: q\nShutting down.\nThe system is halted.")

# test = 'p uw-testbin/widefork;q'
test = "p uw-testbin/pidcheck;q"

for r in range(2000):
	output = subprocess.run(['sys161', 'kernel-ASST2', test], capture_output=True, text=True).stdout
	if expected.match(output):
	# if expected not in output:
		p = output + "\n" + "FAILED"
		sys.exit(p)
	else: 
		print(str(r))

print("Done all tests on " + test)

