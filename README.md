# Constraints-and-EDFs

This directory contains all of the code used in my Senior Honours Project "Application of Constraint Solving to External Difference Families and Related Structures". [GAP](https://www.gap-system.org/) is used to generate valid parameter sets for EDFs, [Essence/Conjure](https://conjure.readthedocs.io/en/latest/) is used to model these parameter sets as constraint problems and search for solutions; and Python is used to verify solutions and print information about them, as well as for basic scripting.


## Installation

- [Conjure installation](https://conjure.readthedocs.io/en/latest/installation.html)
- [GAP installation](https://www.gap-system.org/Download/)
- Install the ``pythonedfs`` package locally using

```
pip3 install -e python/pythonedfs
```

## Usage
The focus of the project was more on obtaining specific results than engineering a generalised searching framework. 
An example of specific actions taken for search for in groups up to size 10 is given here.

**Search for all RWEDFs in groups up to size 10**
1. Ensure the ``gap/params`` is directory clear and there are no pre-existing conjure output files.
2. Use GAP to generate the parameter sets
```
cd gap; gap make_rwedf_params.g
gap> buildAllRWEDFParamsForAllGroups(10);
gap> quit;
cd ..
```
3. Use python to automate running of essence scripts (this may take some time)
```
python3 python/runsearch.py --allmodels --rwedf
```
4. Collect the results into a JSON file
```
python3 python/runsearch.py --rwedf --cleanoutput found_rwedfs.json
```

5. (Optionally) run another script to convert the JSON file into a LaTeX table
```
python3 python/scripts/print_rwedfs.py > rwedftable.tex
```
