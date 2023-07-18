#!/bin/bash

# We generate a random example
a=$(python3 ../../example_generator.py -rc -f temp.dat)

# We execute and stock the OPL result
output=$(oplrun ../program.mod temp.dat)

# We keep the value of the line containing the value of the objective
target_line=$(echo "$output" | grep "^La valeur de l'objectif est de")
 
# We extract the integer at the end of the line 
target_value=$(echo "$target_line" | awk '{print $NF}')

# We store the result from the dynamic programming algorithm
dp_value=$(./build/src/dp_implementation < temp.dat)

# VWe verify if both values are equal
if [ "$target_value" -eq "$dp_value" ]; then
  echo "Results are equal : " $dp_value
else
  echo "Results are differents."
  echo "DP value : " $dp_value
  echo "OPL value : " $target_value
fi

