# -*- coding: utf-8 -*-

import shlex, sys

version = 0

code = ""

istream = sys.stdin

ostream = sys.stdout

collect = False

tapesize = 30000

cellupper = 255
celllower = 0
cellsize = 256

compile = False

translate = None

newline = False

verbose = False
vbflag = ""

stages = False

pause = False

def process_args(args = sys.argv[1:]):
    global version, code, istream, ostream, collect, tapesize, cellupper, celllower, cellsize, compile, newline, verbose, vbflag, stages, pause, translate
    index = 0
    while index < len(args):
        if args[index] in ["-v", "--version"]:
            index += 1
            try:
                version = int(args[index])
            except IndexError:
                raise SystemExit("-v or --version needs an argument!")
            except ValueError:
                raise SystemExit("'%s' is not a number!" % args[index])
        if args[index] in ["-i", "--input"]:
            index += 1
            try:
                istream = open(args[index], "r")
            except IndexError:
                raise SystemExit("-i or --input needs an argument!")
            except FileNotFoundError:
                raise SystemExit("File '%s' not found!" % args[index])
        if args[index] in ["-o", "--output"]:
            index += 1
            try:
                ostream = open(args[index], "w+")
            except IndexError:
                raise SystemExit("-o or --output needs an argument!")
        if args[index] in ["-f", "--file"]:
            index += 1
            try:
                with open(args[index], "r") as f:
                    code = f.read()
            except IndexError:
                raise SystemExit("-f or --file needs an argument!")
            except FileNotFoundError:
                raise SystemExit("File '%s' not found!" % args[index])
        if args[index] in ["-c", "--code"]:
            index += 1
            try:
                code = args[index]
            except IndexError:
                raise SystemExit("-c or --code needs an argument!")
        if args[index] in ["-T", "--tapesize"]:
            index += 1
            try:
                tapesize = int(args[index])
            except IndexError:
                raise SystemExit("-T or --tapesize needs an argument!")
            except ValueError:
                raise SystemExit("'%s' is not a number!" % args[index])
        if args[index] in ["-U", "--upper"]:
            index += 1
            try:
                cellupper = int(args[index])
                cellsize = cellupper - celllower + 1
            except IndexError:
                raise SystemExit("-U or --upper needs an argument!")
            except ValueError:
                raise SystemExit("'%s' is not a number!" % args[index])
        if args[index] in ["-L", "--lower"]:
            index += 1
            try:
                celllower = int(args[index])
                cellsize = cellupper - celllower + 1
            except IndexError:
                raise SystemExit("-L or --lower needs an argument!")
            except ValueError:
                raise SystemExit("'%s' is not a number!" % args[index])
        if args[index] in ["-C", "--collect"]:
            collect = True
        if args[index] in ["--compile"]:
            compile = True
        if args[index] in ["--translate"]:
            index += 1
            try:
                translate = args[index].lower()
            except IndexError:
                raise SystemExit("--translate needs an argument!")
            if translate not in ["c++"]:
                raise SystemExit("Translation only supported into C++!")
        if args[index] in ["--verbose"]:
            verbose = True
        if args[index] in ["--vbflag"]:
            index += 1
            vbflag = args[index]
        if args[index] in ["--stages"]:
            stages = True
        if args[index] in ["-p", "--pause"]:
            pause = True
        if args[index] in ["-n", "--newline"]:
            newline = True
        if args[index] in ["-h", "--help"]:
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
--translate <language>     : Translate the resulting brainfuck code into that
                             language and output the resulting code instead.
--verbose                  : Display verbose output (best used with --collect
                             so that the verbose output does not mangle the
                             program output).
--vbflag                   : Display verbose output when the flag is located in
                             the code.
--stages                   : Display each stage of compilation.
--pause                    : Pause after each stage (doesn't work without some
                             verbosity).
-n --newline               : Output a newline at the end.
-h --help                  : Display this message.

Setting the upper and lower bounds equal to each other makes cells unbounded.

If the code isn't specified by --file or --code, it will be read from STDIN,
        EOF-terminated.
If the input isn't specified by --input, it will be read from STDIN after the
        code. Also, if the program demands more input than the file offers, more
        input will be read from STDIN.
If the output isn't specified by --output, it will be output to STDOUT.\
            """)
        index += 1

process_args()

if code is None:
    code = sys.stdin.read()

if version != 0:
    for v in range(version, 0, -1):
        if stages:
            ostream.write("Version %d: %s" % (v, code) + "\n")
        code = __import__("BF%d" % v).compile(code, **{
            name: globals()[name] for name in ["version", "istream", "ostream", "collect", "tapesize", "cellupper", "celllower", "cellsize", "compile", "newline", "verbose", "vbflag", "stages", "pause"]
        })
        if isinstance(code, tuple):
            process_args(shlex.split(code[1]))
            code = code[0]

if stages:
    ostream.write("Version %d: %s" % (0, code) + "\n")

if translate:
    runs = []
    last = ""
    runlength = 0
    code = "".join(char for char in code if char in "[]><+-.,")
    for char in code:
        if char in "[]><+-.,":
            if char == last:
                runlength += 1
            else:
                if last:
                    runs.append((last, runlength))
                last = char
                runlength = 1
    if last and runlength:
        runs.append((last, runlength))

    if translate.lower() == "c++":
        incode = ""
        for char, run in runs:
            if char == "[":
                incode += "while(t[p]){" * run
            elif char == "]":
                incode += "}" * run
            elif char == "+":
                incode += "t[p]=w(t[p]+%d);" % run
            elif char == "-":
                incode += "t[p]=w(t[p]-%d);" % run
            elif char == ">":
                incode += "p=W(p+%d);" % run
            elif char == "<":
                incode += "p=W(p-%d);" % run
            elif char == ".":
                incode += "P(t[p]);" * run
            elif char == ",":
                incode += "t[p]=G();" * run

        ostream.write("""\
#include<bits/stdc++.h>
#define P std::putchar
#define G std::getchar
long long int t[%d];int p=0;int W(int x){return(x%%%d+%d)%%%d;}int w(int x){return((x-%d)%%%d+%d)%%%d+%d;}int main(){%s}\
        """ % (
            tapesize,
            tapesize,
            tapesize,
            tapesize,
            celllower,
            cellsize,
            cellsize,
            cellsize,
            celllower,
            incode
        ))
        if newline:
            ostream.write("\n")
        ostream.flush()
        ostream.close()
        sys.exit(0)

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
    global buffer
    if collect:
        buffer += chr(val)
    else:
        ostream.write(chr(val))

def shiftleft():
    global pointer
    if tapesize:
        pointer = (pointer - 1) % tapesize
    elif pointer == 0:
        tape = [0] + tape
    else:
        pointer -= 1

def shiftright():
    global pointer
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

if compile:
    ostream.write(code)
    if newline:
        ostream.write("\n")
    ostream.flush()
    ostream.close()
    sys.exit(0)

if celllower > cellupper:
    raise SystemExit("Lower bound cannot exceed upper bound!")

if not (celllower == cellupper or celllower <= 0 <= cellupper):
    raise SystemExit("Cells must either be unbounded or allow 0 as a value!")

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
    if verbose or vbflag and code[index:index + len(vbflag)] == vbflag:
        cells = [("\033[7m%d\033[0m" if i == pointer else "%d") % v for i, v in enumerate(tape)]
        output = ""
        for i, c in enumerate(cells):
            output += c
            if i % 4 == 3 and version >= 2:
                output += "|"
            else:
                output += " "
        (input if pause else print)(output)
    index += 1

ostream.write(buffer)
if newline:
    ostream.write("\n")
ostream.flush()
ostream.close()
