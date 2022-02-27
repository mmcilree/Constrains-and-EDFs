from setfamily import *
from functools import reduce
import sys

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def im_sets(sedf, mod):
    return [list(set([x % mod for x in s])) for s in sedf]

for k in range(7, 100):
    n = k**2 + 1
    if len(factors(n)) == 2:
        continue

    sets = [[x for x in range(k)], [k*x for x in range(1, k+1)]]
    print("SEDF = " + str(sets))
    print("N = " + str(n))
    sedf = CyclicSetFamily(sets, mod=n)
    print("check? = " + str(sedf.is_sedf()))
    print("------")

    for mod in factors(n):
        if mod == 1 or mod == n:
            continue

        im = im_sets(sets, mod)
        print("Image = " + str(im))
        im_family = CyclicSetFamily(im, mod)
        res = im_family.is_sedf()
        if not res:
            print("OOOOH")
            sys.exit()

        print("OEDF? " + str(im_family.is_sedf()))
        print("")
    print("\n")



