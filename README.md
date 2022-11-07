
# Blockchain Demo :link:

A demonstration of blockchain technology in Python3.

## Dependencies
Use `python3 -m pip install -r ./requirements.txt` to install the necessary python packages.

## Running
There are two entry points in this project: `src/main.py` and `src/querier.py`. Both can be run with `python3 <target>`.

- `src/main.py` initializes a blockchain instance and some simulated transaction clients in accordance with a few parameters defined in-line. You should begin to see blocks being appended to the chain.
- `src/querier.py` is a simple command line tool for inspecting particular blocks on the chain in a more human-friendly format. 
