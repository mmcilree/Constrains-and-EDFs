Read("make_params.g");

for n in [20..30] do
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