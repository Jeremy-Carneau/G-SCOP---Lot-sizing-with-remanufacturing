#!/bin/bash

../example_generator.py -rc -f temp.dat
oplrun program.mod temp.dat > temp.txt
../../graph/graph_generation.py temp.txt
