allocate-cell a
allocate-cell b
allocate-cell c
allocate-cell swap

goto-cell cell-of a
,

goto-cell cell-of b
,

copy-cell cell-of a cell-of c cell-of swap
goto-cell cell-of c
.

copy-cell cell-of b cell-of c cell-of swap
goto-cell cell-of c
.
