#!/bin/bash

# usage : ./graph.sh [program.mod] [exemple.dat]

oplrun $1 $2 > temp.txt
../graph/graph_generation.py temp.txt
rm temp.txt

