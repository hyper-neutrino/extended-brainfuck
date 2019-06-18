# -*- coding: utf-8 -*-

# add basic arithmetic operations

import re

def compile(code, **kwargs):
    # add-cell <x> <y> - add the value of <x> to <y>, destroying <x>
    code = re.sub("add-cell (\\d+) (\\d+)", "goto-cell \\1 [goto-cell \\2 + goto-cell \\1 -] goto-cell \\2", code)
    # add-cell-over <x> <y> <z> - add the value of <x> to <y>, counting the number of overflows in <z>, destroying <x>
    code = re.sub("add-cell-over (\\d+) (\\d+) (\\d+)", "goto-cell \\3 [-] goto-cell \\1 [goto-cell \\2 + copy-swap }+{ [}[-]{-] } [} goto-cell \\3 + goto-cell \\2 }3 [-]] } goto-cell \\1 -] goto-cell \\2", code)
    # sub-cell <x> <y> - subtract the value of <x> from <y>, destroying <x>
    code = re.sub("sub-cell (\\d+) (\\d+)", "goto-cell \\1 [goto-cell \\2 - goto-cell \\1 -] goto-cell \\2", code)
    # sub-cell-over <x> <y> <z> - subtract the value of <x> from <y>, counting the number of overflows in <z>, destroying <x>
    code = re.sub("sub-cell-over (\\d+) (\\d+) (\\d+)", "goto-cell \\3 [-] goto-cell \\1 [goto-cell \\2 - copy-swap }+{ [}[-]{-] } [} goto-cell \\3 + goto-cell \\2 }3 [-]] } goto-cell \\1 -] goto-cell \\2", code)
    return code
