# -*- coding: utf-8 -*-

# add basic arithmetic operations

import re

def compile(code, **kwargs):
    # add-cell <x> <y> - add the value of <y> to <x>, destroying <y>
    code = re.sub("add-cell (\\d+) (\\d+)", "goto-cell \\2 [goto-cell \\1 + goto-cell \\2 -] goto-cell \\1", code)
    # add-cell-over <x> <y> <z> - add the value of <y> to <x>, counting the number of overflows in <z>, destroying <y>
    code = re.sub("add-cell-over (\\d+) (\\d+) (\\d+)", "goto-cell \\3 [-] goto-cell \\2 [goto-cell \\1 + copy-swap }+{ [}[-]{-] } [} goto-cell \\3 + goto-cell \\1 }3 [-]] } goto-cell \\2 -] goto-cell \\1", code)
    # sub-cell <x> <y> - subtract the value of <y> from <x>, destroying <y>
    code = re.sub("sub-cell (\\d+) (\\d+)", "goto-cell \\2 [goto-cell \\1 - goto-cell \\2 -] goto-cell \\1", code)
    # sub-cell-over <x> <y> <z> - add the value of <y> to <x>, counting the number of overflows (underflows) in <z>, destroying <y>
    code = re.sub("sub-cell-over (\\d+) (\\d+) (\\d+)", "goto-cell \\3 [-] goto-cell \\2 [goto-cell \\1 - copy-swap }+{ [}[-]{-] } [} goto-cell \\3 + goto-cell \\1 }3 [-]] } goto-cell \\2 -] goto-cell \\1", code)
    return code
