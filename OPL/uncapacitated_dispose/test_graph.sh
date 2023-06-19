#!/bin/bash

../example_generator.py -rd -f temp.dat
oplrun program.mod temp.dat > temp.txt
../../graph/graph_generation.py temp.txt
rm temp.txt
rm temp.dat

