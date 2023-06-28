#!/bin/bash

../example_generator.py -rcd -f temp.dat
oplrun program.mod temp.dat > temp.txt
../../graph/graph_generation.py temp.txt
