# It's Christmas again !

This repo is my secret tool for generating Secret Santa lists to enjoy your family Christmas!

## A Python package for Secret Santa ?
You like big family events? You have four siblings, and each of them has childrens? Christmas with more than twenty gifts per person isn't your style of celebration? Whatever your reason you want to do a secret santa, but you do not want to pick your son, who you would have offered his favorite toy anyway! This small package provides a means to use a constraint graph encoding forbidden edges (e.g. between you and your son) and generates valid secret santa assignment (the problem may not have any solution though  ...).

## Instructions

### Installation
You can install the package in a virtual environment like so:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Usage
The most basic usage is to run the script on a JSON or GML inpu file. Both are given in the example.
```
secretsanta -i data/example.json
```

If you provide a JSON, it has to have a `family` field, which is a list of list. Each sublist is a constraint clique (e.g. your own family, then your brother's, ...) and no matter the names, they will be considered as different persons. 

If you provide a GML, it has to have the following fields: `id`, `label`, and `name`. It can optionally have a `mail` field, which is required when using the automatic e-mail option.

If you want to be sure your matching is valid, use the `verbose` option in the commandline:
```
secretsanta -i data/example.json -v
```

If you want to automatically send mails to the participants, you need to use a GML as input (with `mail` field for each node). Additionally, you need a `mailconfig.json` (see example)
```
secretsanta -i data/example-2.gml -m example-mail-config.json
```
