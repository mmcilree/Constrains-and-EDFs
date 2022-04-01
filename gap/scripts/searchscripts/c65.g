# See README
Read("make_params.g");
G := SmallGroup(65, 1);
Ns := NormalSubgroups(G);
N := Ns[2];
hom := NaturalHomomorphismByNormalSubgroup(G, N);
H := Image(hom, G);

c65ImParams:= function()
    buildParamsForImageWithValues(G, H, 2, 8, 1, true);
end;

c65FromImParams := function()
    buildParamsFromOEDF(G, H, hom, [[1, 1, 1, 2, 2, 2, 3, 5], [1, 2, 3, 3, 3, 5, 5, 5]], 1, true);
end;



