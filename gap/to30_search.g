Read("make_params.g");
count := 0;
imageParams := function()
    for n in [20..27] do
        options :=  validLambdas(n, true);  
        if IsEmpty(options) then
            continue;
        fi;

        for i in [1..NumberSmallGroups(n)] do
            G := SmallGroup(n, i);
            Ns := NormalSubgroups(G);
            numNs := Length(Ns);
            if numNs = 2 then
                continue;
            fi;
            choice := 1;
            for i in [2..Length(Ns)] do
                N := Ns[i];
                best := Ns[choice];
                if n/Order(N) < 11 and n/Order(N) > n/Order(best) then
                    choice := i;
                fi;
            od;

            N := Ns[choice];
            hom := NaturalHomomorphismByNormalSubgroup(G, N);
            H := Image(hom, G);
            Print(StructureDescription(G), " ", StructureDescription(H), "\n----");
            buildAllParamsForImage(G, H, true);
        od;

    od;
end;

normalParams := function()
   for n in [20..27] do
        options :=  validLambdas(n, true);  
        if IsEmpty(options) then
            continue;
        fi;

        for i in [1..NumberSmallGroups(n)] do
            G := SmallGroup(n, i);
            
            buildAllParamsForGroup(G, true);
        od;

    od;
end;

fromImParams := function(im, G, h, hom, lambda)
    buildParamsFromOEDF(G, H, hom, im, lambda, true, String(count));
    count := count + 1;
end;

allImageParams := function()
    local jsonData, r;
    jsonData := JsonStringToGap(StringFile("./upto30images.json"));
    for r in jsonData do
        if r.overgroup[1] < 28 then
            n := r.overgroup[1];
            G := SmallGroup(r.overgroup[1], r.overgroup[2]);
            Ns := NormalSubgroups(G);
            numNs := Length(Ns);
            if numNs = 2 then
                continue;
            fi;
            choice := 1;
            for i in [2..Length(Ns)] do
                N := Ns[i];
                best := Ns[choice];
                if n/Order(N) < 11 and n/Order(N) > n/Order(best) then
                    choice := i;
                fi;
            od;

            N := Ns[choice];
            hom := NaturalHomomorphismByNormalSubgroup(G, N);
            H := Image(hom, G);
            lambda := r.dups*r.subgroup[1]/r.overgroup[1];
            fromImParams(r.osedf,G, H, hom, lambda);
        fi;
    od;
end;
