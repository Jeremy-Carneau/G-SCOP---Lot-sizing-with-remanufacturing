#!/usr/bin/python3

"""
Generate a .dat file following type of lot sizing problem we are working on.
All the values are integers.
The realisability of the example isn't guaranteed.
Enter `./example_generator -h` for help.
"""

##### Imports

import argparse
import random as rd

##### Global variables

Ds_mean = 10 # Mean of the remanufactured demand
Ds_range = 5 # Range of the remanufactured demand

Dn_mean = 15 # Mean of the manufactured demand
Dn_range = 7 # Range of the manufactured demand

R_mean = 20 # Mean of the number of returns
R_range = 8 # Range of the number of returns

C_mean = 50 # Mean of the capacity values
C_range = 5 # Range of the capacity values

f_mean = 50 # Mean of setup cost
f_range = 8 # Range of setup cost

pn_mean = 10 # Mean of variable manufacturing cost
pn_range = 3 # Range of variable manufacturing cost

ps_mean = 7 # Mean of variable remanufacturing cost
ps_range = 2 # Range of variable remanufacturing cost

pr_mean = 4 # Mean of dispose cost
pr_range = 1 # Range of dispose cost

hn_mean = 4 # Mean of holding cost of manufacturing products
hn_range = 1 # Range of holding cost of manufacturing products

hs_mean = 3 # Mean of holding cost of remanufacturing products
hs_range = 2 # Range of holding cost of remanufacturing products

hr_mean = 2 # Mean of holding cost of returns
hr_range = 1 # Range of holding cost of returns

##### Code

def parse_args():
    """ Parse flags and store arguments in the global variable `args`."""
    global args
    parser = argparse.ArgumentParser(description='Generate a .dat file following type of the chosen lot sizing problem. All the values are integers.')
    parser.add_argument("-c", "--capacitated", action="store_true", help="The lot sizing problem include capacity")
    parser.add_argument("-C", action="store_true", help="The capacity is constant (need the capacitated problem)")
    parser.add_argument("-r", "--returns", action="store_true", help="The lot sizing problem include returns")
    parser.add_argument("-d", "--dispose", action="store_true", help="The lot sizing problem include dispose")
    parser.add_argument("-f", "--file", default="example.dat", help="Name of the .dat created file (default : example.dat)")
    parser.add_argument("-T", type=int, default = 30, help="Length of the horizon (default : 30)")
    args = parser.parse_args()
    
def create_random_list(m, r):
    """ Returns a list of random integers in the [m - r, m + r] interval."""
    res = []
    for _ in range(args.T):
        res.append(m + rd.randint(-r, r))
    return res

def adjust_returns(R, Ds):
    """Takes in a list of Returns and a list of demands and adjusts the Returns list so that there exists a solution to the lot sizing problem
    Returns a boolean indicating whether a change has been made or not"""
    pref_R = 0
    pref_Ds = 0
    modified = False
    for i in range(len(R)):
        pref_R += R[i]
        pref_Ds += Ds[i]
        if pref_R>=pref_Ds:
            continue
        modified = True
        while pref_R < pref_Ds:
            delta = R_mean + rd.randint(-R_range, R_range)
            R[i] += delta
            pref_R += delta

    return modified



def generate_example():
    """ Create the .dat file with the constraints set by the problem."""

    file = open(args.file, "w")

    file.write(f"T = {args.T};\n")

    Dn = create_random_list(Dn_mean, Dn_range)
    file.write(f"Dn = {Dn};\n")

    Ds = create_random_list(Ds_mean, Ds_range)
    file.write(f"Ds = {Ds};\n")

    if args.returns:
        R = create_random_list(R_mean, R_range)
        modified = adjust_returns(R, Ds)
        if modified:
            print("The list of returns has been adjusted for a solution to exist")
        file.write(f"R = {R};\n")

    f = create_random_list(f_mean, f_range)
    file.write(f"f = {f};\n")

    pn = create_random_list(pn_mean, pn_range)
    file.write(f"pn = {pn};\n")

    ps = create_random_list(ps_mean, ps_range)
    file.write(f"ps = {ps};\n")

    if args.dispose:
        pr = create_random_list(pr_mean, pr_range)
        file.write(f"pr = {pr};\n")
    
    hn = create_random_list(hn_mean, hn_range)
    file.write(f"hn = {hn};\n")

    hs = create_random_list(hs_mean, hs_range)
    file.write(f"hs = {hs};\n")

    hr = create_random_list(hr_mean, hr_range)
    file.write(f"hr = {hr};\n")

    if args.capacitated:
        if args.C:
            C = [C_mean] * args.T
        else:
            C = create_random_list(C_mean, C_range)
        file.write(f"C = {C};\n")


    file.close()


def main():
    """ Main fonction. Only executed when the script is runned (not imported)."""
    parse_args()
    
    generate_example()

    return 1


if __name__=="__main__":
    main()