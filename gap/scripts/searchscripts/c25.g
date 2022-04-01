# See README
Read("make_params.g");
LoadPackage("json");

G := SmallGroup(25, 2);
Ns := NormalSubgroups(G);
N := Ns[2];
hom := NaturalHomomorphismByNormalSubgroup(G, N);
H := Image(hom, G);
count := 0;

c25Params:= function()
    buildParamsWithValues(G, 2, 12, 6, true);
end;
c25ImParams:= function()
    buildParamsForImageWithValues(G, H, 2, 12, 6, true);
end;

c25FromImParams := function(im)
    buildParamsFromOEDF(G, H, hom, im, 6, true, String(count));
    count := count + 1;
end;

allC25ImParams := function()
    local jsonData, r;
    jsonData := JsonStringToGap(StringFile("./c25images.json"));
    for r in jsonData do
        if r.overgroup[1] = 25 then
            c25FromImParams(r.osedf);
        fi;
    od;
end;

