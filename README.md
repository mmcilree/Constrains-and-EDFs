# Constraints-and-EDFs

This directory contains all of the code used in my Senior Honours Project "Application of Constraint Solving to External Difference Families and Related Structures". [GAP](https://www.gap-system.org/) is used to generate valid parameter sets for EDFs, [Essence/Conjure](https://conjure.readthedocs.io/en/latest/) is used to model these parameter sets as constraint problems and search for solutions; and Python is used to verify solutions and print information about them.


## Installation

- [Conjure installation](https://conjure.readthedocs.io/en/latest/installation.html)
- [GAP installation](https://www.gap-system.org/Download/)
- Install the ``pythonedfs`` package locally using

```
pip3 install -e python/pythonedfs
```

## Usage
The focus of the project was more on obtaining specific results than engineering a generalised searching framework. The specific actions taken to reproduce the results in the report are therefore listed here, but a general interface/automation mechanism is not supplied.