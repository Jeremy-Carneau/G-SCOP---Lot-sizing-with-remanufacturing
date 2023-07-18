#!/bin/bash

python3.11 ../example_generator.py -rc -f temp.dat
oplrun program.mod temp.dat > temp.txt
grep "^La valeur de l'objectif est de" temp.txt
./dp_implementation < temp.dat