# -*- coding: utf-8 -*-

# Writing a number after a command (with arbitrary whitespace in between) will repeat that command that many times

import re

def compile(code):
    return re.sub("[+-.,<>\\[\\]]\\s*\\d+", lambda s: s.group()[0] * int(s.group()[1:].strip()), code)
