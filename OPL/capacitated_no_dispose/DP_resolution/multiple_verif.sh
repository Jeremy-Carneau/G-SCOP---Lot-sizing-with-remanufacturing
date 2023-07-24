#!/bin/bash

counter=0
max_iterations=100

# We execute at most 20 iterations of the verification program
while [ $counter -lt $max_iterations ]; do
    output=$(./verify_dp.sh)
    
    # If the results are the same
    if echo "$output" | grep -q "Results are equal : "; then
        echo "Exact."

    # If the results are differents
    elif echo "$output" | grep -q "Results are differents."; then
        echo "Error :" 
        echo "$output"
        break
    fi
    
    ((counter++))
done
