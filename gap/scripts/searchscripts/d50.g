# See README
Read("make_params.g");
LoadPackage("json");

G := SmallGroup(50, 1);
Ns := NormalSubgroups(G);
N := Ns[3];
hom := NaturalHomomorphismByNormalSubgroup(G, N);
H := Image(hom, G);
count := 0;

d50Params:= function()
    buildParamsWithValues(G, 2, 7, 1, true);
end;
d50ImParams:= function()
    buildParamsForImageWithValues(G, H, 2, 7, 1, true);
end;

d50FromImParams := function(im)
    buildParamsFromOEDF(G, H, hom, im, 1, true, String(count));
    count := count + 1;
end;

alld50ImParams := function()
    local jsonData, r;
    jsonData := JsonStringToGap(StringFile("./d50images.json"));
    for r in jsonData do
        if r.overgroup[1] = 50 then
            d50FromImParams(r.osedf);
        fi;
    od;
end;

