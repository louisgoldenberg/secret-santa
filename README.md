# It's Christmas again !

This repo is my secret tool for generating Secret Santa permutations!

## Instructions
For privacy reasons, I did not include my own family graph in the repo, but simply provided an example in data/example.json and data/example.gml.
Simply run the program on a similar file:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python src/secret-santa/main.py -i example.json
```
