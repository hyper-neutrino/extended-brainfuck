# -*- coding: utf-8 -*-

# add better memory management

import re

def compile(code, **kwargs):
    allocated = {}
    cell = 0
    for name in re.findall("allocate-cell ([A-Za-z0-9_]+)", code):
        if name not in allocated:
            allocated[name] = cell
            cell += 1
    code = re.sub("allocate-cell ([A-Za-z0-9_]+)", "", code)
    code = re.sub("cell-of ([A-Za-z0-9_]+)", lambda s: str(allocated[s.group(1)]), code)
    code = re.sub("`([A-Za-z0-9_]+)`", lambda s: str(allocated[s.group(1)]), code)
    return (code, "--tapesize %d" % cell)
