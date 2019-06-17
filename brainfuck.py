# -*- coding: utf-8 -*-

import sys

version = "0"

code = ""

istream = sys.stdin

ostream = sys.stdout

collect = False

index = 0

tapesize = 30000

cellupper = 255
celllower = 0

compile = False

newline = False

while index < len(sys.argv) - 1:
    index += 1
    if sys.argv[index] in ["-v", "--version"]:
        index += 1
        try:
            version = sys.argv[index]
        except IndexError:
            raise SystemExit("-v or --version needs an argument!")
    if sys.argv[index] in ["-i", "--input"]:
        index += 1
        try:
            istream = open(sys.argv[index], "r")
        except IndexError:
            raise SystemExit("-i or --input needs an argument!")
        except FileNotFoundError:
            raise SystemExit("File '%s' not found!" % sys.argv[index])
    if sys.argv[index] in ["-o", "--output"]:
        index += 1
        try:
            ostream = open(sys.argv[index], "w+")
        except IndexError:
            raise SystemExit("-o or --output needs an argument!")
    if sys.argv[index] in ["-f", "--file"]:
        index += 1
        try:
            with open(sys.argv[index], "r") as f:
                code = f.read()
        except IndexError:
            raise SystemExit("-f or --file needs an argument!")
        except FileNotFoundError:
            raise SystemExit("File '%s' not found!" % sys.argv[index])
    if sys.argv[index] in ["-c", "--code"]:
        index += 1
        try:
            code = sys.argv[index]
        except IndexError:
            raise SystemExit("-c or --code needs an argument!")
    if sys.argv[index] in ["-T", "--tapesize"]:
        index += 1
        try:
            tapesize = int(sys.argv[index])
        except IndexError:
            raise SystemExit("-T or --tapesize needs an argument!")
        except ValueError:
            raise SystemExit("'%s' is not a number!" % sys.argv[index])
    if sys.argv[index] in ["-U", "--upper"]:
        index += 1
        try:
            cellupper = int(sys.argv[index])
        except IndexError:
            raise SystemExit("-U or --upper needs an argument!")
        except ValueError:
            raise SystemExit("'%s' is not a number!" % sys.argv[index])
    if sys.argv[index] in ["-L", "--lower"]:
        index += 1
        try:
            celllower = int(sys.argv[index])
        except IndexError:
            raise SystemExit("-L or --lower needs an argument!")
        except ValueError:
            raise SystemExit("'%s' is not a number!" % sys.argv[index])
    if sys.argv[index] in ["-C", "--collect"]:
        collect = True
    if sys.argv[index] in ["--compile"]:
        compile = True
    if sys.argv[index] in ["-n", "--newline"]:
        newline = True
    if sys.argv[index] in ["-h", "--help"]:
        raise SystemExit("""\
-v --version  <version number>: Run the specified version.
-i --input    <file name>  : Read input from the specified file (using STDIN if
                             more is needed).
-o --output   <file name>  : Write output to the specified file (overwrites
                             existing content!).
-f --file     <file name>  : Run code from the specified file.
-c --code     <code>       : Run the specified code.
-T --tapesize <tape size>  : Set the size of the tape (default 30000, 0 means
                             unbounded).
-U --upper    <upper bound>: Set the maximum cell value (default 255).
-L --lower    <lower bound>: Set the minimum cell value (default 0).
-C --collect               : Collect all of the output to display at the end to
                             prevent I/O from getting mangled in the terminal.
--compile                  : Compile the code and output it instead of running
                             the program.
-n --newline               : Output a newline at the end.
-h --help                  : Display this message.

Setting the upper and lower bounds equal to each other makes cells unbounded.

If the code isn't specified by --file or --code, it will be read from STDIN,
        EOF-terminated.
If the input isn't specified by --input, it will be read from STDIN after the
        code. Also, if the program demands more input than the file offers, more
        input will be read from STDIN.
If the output isn't specified by --output, it will be output to STDOUT.""")

cellsize = cellupper - celllower + 1

if code is None:
    code = sys.stdin.read()

buffer = ""

tape = [0] * (tapesize or 1)

pointer = 0

def getchar():
    char = istream.read(1)
    if char == "":
        char = sys.stdin.read(1)
    val = ord(char)
    if cellupper == celllower:
        return val
    val -= celllower
    val %= cellsize
    val += celllower
    return val

def putchar(val):
    if collect:
        buffer += chr(val)
    else:
        ostream.write(chr(val))

def shiftleft():
    if tapesize:
        pointer = (pointer - 1) % tapesize
    elif pointer == 0:
        tape = [0] + tape
    else:
        pointer -= 1

def shiftright():
    pointer += 1
    if tapesize:
        pointer %= tapesize
    elif pointer == len(tape):
        tape.append(0)

def increment():
    tape[pointer] += 1
    if cellupper == celllower:
        return
    if tape[pointer] > cellupper:
        tape[pointer] -= cellsize

def decrement():
    tape[pointer] -= 1
    if cellupper == celllower:
        return
    if tape[pointer] < celllower:
        tape[pointer] += cellsize

jumps = {}

brackets = []
for index, char in enumerate(code):
    if char == "[":
        brackets.append(index)
    if char == "]":
        open_bracket = brackets.pop()
        close_bracket = index
        jumps[open_bracket] = close_bracket
        jumps[close_bracket] = open_bracket

if version != "0":
    code = __import__("BF%s" % version).compile(code)

if compile:
    ostream.write(code)
    if newline:
        ostream.write("\n")
    ostream.flush()
    ostream.close()
    sys.exit(0)

index = 0
while index < len(code):
    if code[index] == "+":
        increment()
    elif code[index] == "-":
        decrement()
    elif code[index] == ">":
        shiftright()
    elif code[index] == "<":
        shiftleft()
    elif code[index] == ",":
        tape[pointer] = getchar()
    elif code[index] == ".":
        putchar(tape[pointer])
    elif code[index] == "[" and tape[pointer] == 0:
        index = jumps[index]
    elif code[index] == "]" and tape[pointer] != 0:
        index = jumps[index] - 1
    index += 1

ostream.write(buffer)
if newline:
    ostream.write("\n")
ostream.flush()
ostream.close()
