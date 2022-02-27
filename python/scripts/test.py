from setfamily import *
from data.testedfs import *

t1 = CyclicSetFamily(p_2_1, 19)
print(str(p_2_1) + ":")

print("Is edf? {0}".format(t1.is_edf()))
print("Is strong edf? {0}".format(t1.is_sedf()))
print("----")

t2 = CyclicSetFamily(non_edf_1, 31)
print(str(non_edf_1) + ":")
print("Is edf? {0}".format(t1.is_edf()))
print("Is strong edf? {0}".format(t1.is_sedf()))
print("----")

for h in h_7_all_with_mods:
    h_sedf = h[0]
    h_mod = h[1]
    if type(h_sedf[0][0]) is tuple:
        th = CyclicProductSetFamily(h_sedf, h_mod)
    else:
        th = CyclicSetFamily(h_sedf, h_mod)

    print(str(h_sedf) + ":")
    print("Is edf? {0}".format(th.is_edf()))
    print("Is strong edf? {0}".format(th.is_sedf()))
    print("----")

t3 = CyclicProductSetFamily(d_3_1, 4)
print(str(d_3_1) + ":")
print("Is edf? {0}".format(t3.is_edf()))
print("Is strong edf? {0}".format(t3.is_sedf()))
print("----")

t4 = SetFamily(j_50, sg_50_1_mult_table)
print(str(j_50) + ":")
print("Is edf? {0}".format(t4.is_edf()))
print("Is strong edf? {0}".format(t4.is_sedf()))
print("----")
t4.print_external_differences(sort_by="value")

t5 = SetFamily(j_10, sg_10_1_mult_table)
print(str(j_10) + ":")
print("Is edf? {0}".format(t5.is_edf()))
print("Is strong edf? {0}".format(t5.is_sedf()))
print("----")
t5.print_external_differences(sort_by="value")