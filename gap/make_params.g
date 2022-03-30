#!/usr/bin/gap -q
Read("utils.g");

# This file contains functions for generating parameters for either a direct EDF/SEDF search
# or an optimised search based on first finding potential homomorphic images of EDFs/SEDFs, termed
# OEDFs or OSEDFs. (oedf used throughout here for brevity).

# Matthew McIlree (2022)

# Convert boolean isSEDF to string "sedf" or "edf"
typeAsString := function(isSEDF)
	local type;
	if isSEDF then
		type := "sedf";
	else
		type := "edf";
	fi;

	return type;
end;

# Return all of the valid lambda values
# Adapted from code provided by Christopher Jefferson (2021)
validLambdas := function(n, sedf)
	local numsets, setsize, lambda, l;
	l := [];
	for numsets in [2..n-1] do
		for setsize in [2..n] do
			if numsets * setsize > n then
				continue;
			fi;

			if sedf then
				lambda := (setsize * setsize * (numsets - 1))/(n-1);
			else
				lambda := (setsize * setsize * numsets * (numsets - 1))/(n-1);
			fi;

			if IsInt(lambda) then
				Add(l, rec(setsize := setsize, numsets := numsets, lambda := lambda));
			fi;
		od;
	od;
	return l;
end;


# Print an Essence .param file: 
# Adapted from code provided by Christopher Jefferson (2021)
# This has been adapated to allow for EDF images (OMSEDFs), and EDFs based on those images. 
outputEssenceFile := function(filename, ordgrp, s, tables, symlist, setsize, numsets, lambda, sedf, allowedVals)
	local output;
	output := OutputTextFile(filename, false );
	SetPrintFormattingStatus(output, false);
	PrintToFormatted(output, "letting n be {}\n", Length(ordgrp));

	# For an p
	if s <> false then
		PrintToFormatted(output, "letting s be {}\n", s);
	fi;

	# If restricting values based on an imagel, add an allowedvalues parameter
	if allowedVals <> false then
		PrintToFormatted(output, "letting allowedvalues be {}\n", allowedVals);
	fi;

	PrintToFormatted(output, "letting inverses be {}\n", tables.inverses);
	PrintToFormatted(output, "letting multable be {}\n", tables.multable);
	PrintToFormatted(output, "letting mulinvtable be {}\n", tables.mulinvtable);
	PrintToFormatted(output, "letting multuples be {}\n", tables.multuples);
	PrintToFormatted(output, "letting mulinvtuples be {}\n", tables.mulinvtuples);
	PrintToFormatted(output, "letting setsize be {}\n", setsize);
	PrintToFormatted(output, "letting setnum be {}\n", numsets);
	PrintToFormatted(output, "letting dups be {}\n", lambda);
	

	if symlist <> false then
		PrintToFormatted(output, "letting symsize be {}\n", Size(symlist));
		PrintToFormatted(output, "letting syms be {}\n", List(symlist, l -> List(l, x -> x)));
	fi;
	
	PrintToFormatted(output, "letting makeEDF be false\n", not sedf);
	PrintToFormatted(output, "letting makeSEDF be true\n", sedf);
	
	CloseStream(output);
end;

# Get some reusable information about the group.
getGroupData := function(group)
	local data, ordElms, name;

	ordElms := OrderedElements(group);
	name := StructureDescription(group);
	RemoveCharacters(name," ");

	data := rec(
		name := name,
		id := IdSmallGroup(group)[2],
		elements := ordElms,
		size := Order(group),
		syms := CollectSyms(ordElms, 1000),
		tables := BuildTables(ordElms)
	);

	return data;
end;

# Create all possible .param files for this particular group.
buildAllParamsForGroup := function(group, isSEDF)
	local g, o, options, type, option, filename;
	
	g := getGroupData(group);
	type := typeAsString(isSEDF);
	options := validLambdas(g.size, isSEDF);

	for o in options do
		filename := StringFormatted("params/{}_{}_{}_{}_{}_{}.param", type, g.size, g.id, o.numsets, o.setsize, o.lambda);
		outputEssenceFile(filename, g.elements, false, g.tables, g.syms, o.setsize, o.numsets, o.lambda, isSEDF, false);
	od;
end;

# Create a .param file for these particular values
buildParamsWithValues := function(group, numSets, setSize, lambda, isSEDF)
	local g, type, filename;

	g := getGroupData(group);
	type := typeAsString(isSEDF);
	filename := StringFormatted("params/{}_{}_{}_{}_{}_{}.param", type, g.size, g.id, numSets, setSize, lambda);

	outputEssenceFile(filename, g.elements, false, g.tables, g.syms, setSize, numSets, lambda, isSEDF, false);
end;

# Convert an OEDF (possible image) into a list of allowed values for each position in the EDF
getAllowedVals := function(group, image, oedf, hom)
	local set, value, allowedVals, allowed, imEls, gEls, el, i, j, k;
	gEls := OrderedElements(group);
	imEls := OrderedElements(image);

	# allowedValues[i][j][k] should be a boolean indicating whether the jth position in ith set
	# can take the kth value in the ordered elements of the group.
	allowedVals := [];

	i := 1;
	for set in oedf do
		Add(allowedVals, []);
		j := 1;
		for value in set do
			Add(allowedVals[i], []);
			el := imEls[value];
			allowed := PreImages(hom, el);
			for k in [1..Size(group)] do;
				if gEls[k] in allowed then
					Add(allowedVals[i][j], true);
				else	
					Add(allowedVals[i][j], false);
				fi;
			od;
			j := j +1;
		od;
		i := i +1;
	od;

	return allowedVals;
end;

# Build .params constrained to being and EDF that maps to a particular possible image under a homomorphism.
buildParamsFromOEDF := function(group, image, hom, oedf, lambda, isSEDF, tag)
	local g, type, filename, numSets, setSize, allowedVals;
	# hom := NaturalHomomorphismByNormalSubgroup(group, image);
	numSets := Size(oedf);
	setSize := Size(oedf[1]);

	g := getGroupData(group);
	allowedVals := getAllowedVals(group, image, oedf, hom);
	type := typeAsString(isSEDF);

	filename := StringFormatted("params/{}{}_{}_{}_{}_{}_{}.param", type, g.size, g.id, numSets, setSize, lambda, tag);
	outputEssenceFile(filename, g.elements, false, g.tables, false, setSize, numSets, lambda, isSEDF, allowedVals);
end;

# Create all possible param files for a particular image group (under some homomorphism).
# Note that the group 'image' should be isomorphic to the quotient G/N for some quotient group N.
buildAllParamsForImage := function(group, image, isSEDF)
	local g, o, i, type, lambda, filename, options;
	g := getGroupData(group);
	i := getGroupData(image);
	type := Concatenation("o", typeAsString(isSEDF));
	options := validLambdas(g.size, isSEDF);

	for o in options do
		lambda := o.lambda*(g.size/i.size);
		filename := StringFormatted("params/{}_{}_{}_{}_{}_{}_{}_{}.param", type, g.size, g.id, i.size, i.id, o.numsets, o.setsize, lambda);
		outputEssenceFile(filename, i.elements, g.size, i.tables, false, o.setsize, o.numsets, lambda, isSEDF, false);
	od;
end;

# Create .param file for a potential image, with a particular original group in mind.
buildParamsForImageWithValues := function(group, image, numsets, setsize, lambda, isSEDF)
	local g, o, i, type, filename, options;
	g := getGroupData(group);
	i := getGroupData(image);
	type := Concatenation("o", typeAsString(isSEDF));

	lambda := lambda*(g.size/i.size);
	filename := StringFormatted("params/{}_{}_{}_{}_{}_{}_{}_{}.param", type, g.size, g.id, i.size, i.id, numsets, setsize, lambda);
	outputEssenceFile(filename, i.elements, g.size, i.tables, false, setsize, numsets, lambda, isSEDF, false);

end;

# Create .param files for a potential image, restricted in turn by another image
# (Unused in the end in the project but demonstrates the concept).
buildParamsForImageFromOEDF := function(overgroup, group, image, hom, oedf, lambda, isSEDF)
	local g, og, type, filename, numSets, setSize, allowedVals;
	numSets := Size(oedf);
	setSize := Size(oedf[1]);

	og := getGroupData(overgroup);
	g := getGroupData(group);
	allowedVals := getAllowedVals(group, image, oedf, hom);
	type := Concatenation("o", typeAsString(isSEDF));

	filename := StringFormatted("params/{}_{}_{}_{}_{}_{}_{}_{}.param", type, og.size, og.id, g.size, g.id, numSets, setSize, lambda);
	outputEssenceFile(filename, g.elements, og.size, g.tables, false, setSize, numSets, lambda, isSEDF, allowedVals);
end;