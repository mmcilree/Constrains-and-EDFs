Read("make_params.g");
LoadPackage("json");

G := SmallGroup(21, 2);
Ns := NormalSubgroups(G);
N := Ns[2];
hom := NaturalHomomorphismByNormalSubgroup(G, N);
H := Image(hom, G);
count := 0;

c21Params:= function()
    buildParamsWithValues(G, 2, 10, 5, true);
end;

c21ImParams:= function()
    buildParamsForImageWithValues(G, H, 2, 10, 5, true);
end;

c21FromImParams := function(im)
    buildParamsFromOEDF(G, H, hom, im, 6, true, String(count));
    count := count + 1;
end;

allC21ImParams := function()
    local jsonData, r;
    jsonData := JsonStringToGap(StringFile("./c21images.json"));
    for r in jsonData do
        if r.overgroup[1] = 21 then
            c21FromImParams(r.osedf);
        fi;
    od;
end;

