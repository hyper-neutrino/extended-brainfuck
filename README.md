# Brainfuck

Brainfuck is a very simple yet Turing complete 8-instruction language invented by Urban Muller in 1993 in an attempt to make the smallest compiler for the language. It has a memory tape of integer cells with 8 operations:

- `+` - increment the memory cell
- `-` - decrement the memory cell
- `>` - shift the memory pointer to the right
- `<` - shift the memory pointer to the left
- `,` - read a character of input and put its ASCII value into the memory cell
- `.` - write the current memory cell as a character
- `[` - if the memory cell is 0, jump past the matching `]`
- `]` - if the memory cell is not 0, jump to the matching `[`

(`[...]` is basically a while loop that checks the current memory cell each time).

This language is Turing complete, meaning technically any program can be run with it; however, it is known as a "Turing tarpit", meaning that it is extremely difficult to do most sane things.

For example, the `cat` program in brainfuck would just be `,[.,]`, which takes input and repeatedly outputs and inputs while the input is not 0.

# Brainfuck - Extension 1

The first extension allows you to more easily repeat commands. Since you can only increase/decrease memory cells and shift memory pointers by one each time, you often need to write many `+`, `-`, `<`, or `>` operations in a row. In this extension, writing any command followed by an integer will translate into that command repeated that many times.

# Brainfuck - Extension 2

The second extension indexes the cells, allowing you to jump to arbitrary memory positions (albeit very slowly). Each memory block contains four cells and `>` and `<` are redefined to mean `>4` and `<4`. This extension defines `goto-cell <x>`, which jumps to the `x`<sup>th</sup> 0-indexed cell, with `goto-zero` being an alias for `goto-cell 0`, both of which run more efficiently than other goto operations.

The memory blocks contain four values each: the cell value, followed by the cell index, followed by two swap spaces. `copy-swap` takes the current value and copies it into the first swap, overwriting the second swap in the process. `zero-swaps` clears both of the swap spaces.

Finally, `copy-cell <x> <y> <z>` copies the value of `<x>` to `<y>`, destroying `<z>`.

# Brainfuck - Extension 3

The third extension implements some basic arithmetic operations:

- `add-cell <x> <y>` - add the value of `<x>` to `<y>`, destroying `<x>`
- `add-cell-over <x> <y> <z>` - add the value of `<x>` to `<y>`, destroying `<x>`, counting overflows in `<z>`
- `sub-cell <x> <y>` - subtract the value of `<x>` from `<y>`, destroying `<x>`
- `sub-cell-over <x> <y> <z>` - subtract the value of `<x>` from `<y>`, destroying `<x>`, counting overflows in `<z>`

# Brainfuck - Extension 4

The fourth extension implements better memory management. `allocate-cell <name>` will tell the compiler to associate a cell with `<name>`. Every cell must be `allocate`d; the tape size will be re-bounded to the number of cells needed. `cell-of <name>` and ``\`<name>\``` are translated to the pointer position of the cell. Cell names are enumerated in order of appearance in the code.
