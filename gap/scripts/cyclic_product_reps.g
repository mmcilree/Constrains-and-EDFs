Read("utils.g");

cyclicProductReps := function(n, id, csizes)
    local OG, elms, k, Cs, Cels, DP, iso, projections, components, reps, el;
    OG := SmallGroup(n, id);
    elms := OrderedElements(OG);
    k := Size(csizes);
    Cs := List(csizes, i -> CyclicGroup(i));
    Cels := List(Cs, C -> OrderedElements(C));
    DP := DirectProduct(Cs);
    iso := IsomorphismGroups(OG, DP);
    projections := List([1..k], i -> Projection(DP, i));

    reps := [];
    for el in elms do 
        components := List([1..k], i -> Image(projections[i], Image(iso, el)));
        Add(reps, List([1..k], i -> Position(Cels[i], components[i])-1));
    od;
    return reps;
end;