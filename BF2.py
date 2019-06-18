# -*- coding: utf-8 -*-

# Each cell is expanded to [value, id, swap 1, swap 2]
# Cells should be bound to at least how many cells you will need. Unbounded cells will break when you go too far left.
# Goto does not work if the tape is unbounded because it scans right since you can't detect which direction to go

import re

def compile(code, tapesize, **kwargs):
    # Populate the IDs, if the tape size is not 0
    code = ">" * (tapesize - 1) + "}}}}" + code

    # When right-shifting:
    # - zero the current swap 1
    # - zero the next swap 1
    # - zero the next id
    # - move the current id to the current swap 1 and the next id
    # - move the current swap 1 to the current id
    # - increment the next id
    # - go to the next cell
    code = code.translate({
        ord(">"): ">2[-]>3[-]>[-]<5[>+>3+<4-]>[<+>-]>3+<",
        ord("<"): ">2[-]<4[-]<[-]>4[>+<5+>4-]>[<+>-]<5-<",
        ord("{"): "<",
        ord("}"): ">"
    })
    # To implement jumping:
    # - zero the current swap 1
    # - zero the current swap 2
    # - move the current id to the current swap 1 and the current swap 2
    # - move the current swap 2 to the current id
    # - set the current swap 2 to the requested id
    # - subtract the current swap 1 from the current swap 2
    # - go to the current swap 2
    # - WHILE
    code = re.sub("copy-cell (\\d+) (\\d+) (\\d+)", "goto-cell \\2 [-] goto-cell \\3 [-] goto-cell \\1 [goto-cell \\3 + goto-cell \\1 -] goto-cell \\3 [goto-cell \\2 + goto-cell \\1 + goto-cell \\3 -] goto-cell \\2", code)
    code = code.replace("goto-cell 0", "goto-zero")
    code = re.sub("goto-cell (\\d+)", "<[-]+[>3[-]>[-]<2[>+>+<2-]>2[<2+>2-]+\\1<[>-<-]>]<3", code)
    code = code.replace("goto-zero", ">[<4]<")
    code = code.replace("copy-swap", "zero-swaps [>2+>+<3-]>3[<3+>3-]<")
    code = code.replace("zero-swaps", ">2[-]>[-]<3")
    return (code, "--tapesize %d" % (tapesize * 4))
