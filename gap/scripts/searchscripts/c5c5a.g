# See README
Read("make_params.g");
LoadPackage("json");

G := SmallGroup(25, 2);
Ns := NormalSubgroups(G);
choice := 1;
for i in [2..Length(Ns)] do
    N := Ns[i];
    best := Ns[choice];
    if 25/Order(N) < 11 and 25/Order(N) > 25/Order(best) then
        choice := i;
    fi;
od;

N := Ns[choice];
hom := NaturalHomomorphismByNormalSubgroup(G, N);
H := Image(hom, G);
count := 0;

params:= function()
    buildParamsWithValues(G, 7, 2, 1, true);
end;

imParams:= function()
    buildParamsForImageWithValues(G, H, 7, 2, 1, true);
end;

fromImParams := function(im)
    buildParamsFromOEDF(G, H, hom, im, 1, true, String(count));
    count := count + 1;
end;

allFromImParams := function()
    local jsonData, r;
    jsonData := JsonStringToGap(StringFile("./c5c5aimages.json"));
    for r in jsonData do
        if r.overgroup[1] = 25 then
            fromImParams(r.osedf);
        fi;
    od;
end;

