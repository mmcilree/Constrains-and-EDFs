Read("utils.g");
# This function can be used to write out all the elements of SmallGroup whose
# best representation is a direct product as tuples.

# e.g. SmallGroup(25, 2) = C5xC5 should be [(0, 0), (0, 1) ... (0, 5), (1, 0) ... (4, 4)]
cyclicProductReps := function(n, id, csizes)
    # csizes = list of sizes of terms in the direct product, e.g. C5xC5  = [5, 5]
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