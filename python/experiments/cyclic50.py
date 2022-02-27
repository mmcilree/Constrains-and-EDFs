from ..setfamily import *
sedf = [[0, 1, 2, 3, 4, 5, 6], [7, 14, 21, 28, 35, 42, 49]]

def im_sedf(sedf, mod):
    return [list(set([x % mod for x in s])) for s in sedf]

for mod in [2, 5, 10, 25]:
    im = im_sedf(sedf, mod)
    print("Image = " + str(im))
    im_family = CyclicSetFamily(im, mod)
    print("OEDF? " + str(im_family.is_sedf()))