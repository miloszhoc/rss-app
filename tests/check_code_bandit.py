#!/usr/bin/env python3
import sys

cmd_output = sys.stdin.read()
try:
    assert '' == cmd_output
except AssertionError:
    print(cmd_output)
else:
    pass
