from setfamily import SetFamily

d10_mult = [
    [x - 1 for x in s]
    for s in [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [2, 1, 4, 3, 6, 5, 8, 7, 10, 9],
        [3, 10, 5, 2, 7, 4, 9, 6, 1, 8],
        [4, 9, 6, 1, 8, 3, 10, 5, 2, 7],
        [5, 8, 7, 10, 9, 2, 1, 4, 3, 6],
        [6, 7, 8, 9, 10, 1, 2, 3, 4, 5],
        [7, 6, 9, 8, 1, 10, 3, 2, 5, 4],
        [8, 5, 10, 7, 2, 9, 4, 1, 6, 3],
        [9, 4, 1, 6, 3, 8, 5, 10, 7, 2],
        [10, 3, 2, 5, 4, 7, 6, 9, 8, 1],
    ]
]

d10_names = [
    "e",
    "\\beta",
    "\\alpha",
    "\\beta\\alpha",
    "\\alpha^2",
    "\\beta\\alpha^2",
    "\\alpha^3",
    "\\beta\\alpha^3",
    "\\alpha^4",
    "\\beta\\alpha^4",
]

d10_sets = [ [ 0, 1, 2, 3, 4, 5, 6 ], [ 1, 2, 4, 5, 7, 8, 9 ] ]

d10_edf = SetFamily(d10_sets, d10_mult, elstr=d10_names)
#d10_edf.print_external_differences(sort_by="value", perline=6)
print(d10_edf.is_edf())
print(d10_edf.is_sedf())
d10_edf.print_external_differences_tables()

