# It's Christmas again !

This repo is my secret tool for generating Secret Santa lists to enjoy your family Christmas!

## A Python package for Secret Santa ?
You like big family events? You have four siblings, and each of them has childrens? Christmas with more than twenty gifts per person isn't your style of celebration? Whatever your reason you want to do a secret santa, but you do not want to pick your son, who you would have offered his favorite toy anyway! This small package provides a means to use a constraint graph encoding forbidden edges (e.g. between you and your son) and generates valid secret santa assignment (the problem may not have any solution though  ...).

## Instructions
You can install the package in a virtual environment like so:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```
Then simply run the program on a file (following one of the examples):
```
secretsanta -i example.json
```

If you provide a JSON, it has to have a 'family' field, which is a list of list. Each sublist is a constraint clique (e.g. your own family, then your brother's, ...) and no matter the names, they will be considered as different persons. 

For a more general result, you can directly provide a GML file containing a graph, where you can do something more complicated than a set of disjoint cliques (e.g. why not edges between godfather/godmother and nephew/niece?).