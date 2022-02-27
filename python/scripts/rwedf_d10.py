from setfamily import *
d10_mult = [[x - 1 for x in s] for s in [ [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ], [ 2, 3, 4, 5, 1, 10, 6, 7, 8, 9 ], 
  [ 3, 4, 5, 1, 2, 9, 10, 6, 7, 8 ], [ 4, 5, 1, 2, 3, 8, 9, 10, 6, 7 ], 
  [ 5, 1, 2, 3, 4, 7, 8, 9, 10, 6 ], [ 6, 7, 8, 9, 10, 1, 2, 3, 4, 5 ], 
  [ 7, 8, 9, 10, 6, 5, 1, 2, 3, 4 ], [ 8, 9, 10, 6, 7, 4, 5, 1, 2, 3 ], 
  [ 9, 10, 6, 7, 8, 3, 4, 5, 1, 2 ], [ 10, 6, 7, 8, 9, 2, 3, 4, 5, 1 ] ]]

d10_names = [
    "e",
    "\\alpha",
    "\\alpha^2",
    "\\alpha^3",
    "\\alpha^4",
    "\\beta",
    "\\beta\\alpha",
    "\\beta\\alpha^2",
    "\\beta\\alpha^3",
    "\\beta\\alpha^4",
]

# sets_1 = [[x-1 for x in s] for s in [[1, 2, 6], [3, 4, 9], [7], [8]]]

# rwedf_1 = SetFamily(sets_1, d10_mult, elstr=d10_names)
# print(rwedf_1.latex_str())
# print(rwedf_1.get_external_differences_tables(combine=True))
# for i in range(len(sets_1)):
#     print(rwedf_1.get_Ns_str(i))
# print(rwedf_1.get_rweighted_sums_str())

sets_2 = [[x-1 for x in s] for s in [[1,2], [3, 5], [6], [7], [8], [9], [10]]]

rwedf_2 = SetFamily(sets_2, d10_mult, elstr=d10_names)
print(rwedf_2.latex_str())
print(rwedf_2.get_external_differences_tables(combine=True))
for i in range(len(sets_2)):
    print(rwedf_2.get_Ns_str(i))
print(rwedf_2.get_rweighted_sums_str())
print(rwedf_2.is_rwedf())