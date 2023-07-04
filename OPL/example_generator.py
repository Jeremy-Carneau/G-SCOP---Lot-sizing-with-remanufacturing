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

Ds_mean = 10 # Mean of the remanufactured demand (10)
Ds_range = 5 # Range of the remanufactured demand (5)

Dn_mean = 15 # Mean of the manufactured demand (15)
Dn_range = 7 # Range of the manufactured demand (7)

R_mean = 11 # Mean of the number of returns (11)
R_range = 5 # Range of the number of returns

Cn = 45 # Value of the production capacity of new products
Cs = 30 # Value of the production capacity of remanufactured products

C = 80 # Production capacity in case of common capacity

f_mean = 5000 # Mean of setup cost
f_range = 30 # Range of setup cost

pn_mean = 70 # Mean of variable manufacturing cost
pn_range = 5 # Range of variable manufacturing cost

ps_mean = 47 # Mean of variable remanufacturing cost
ps_range = 3 # Range of variable remanufacturing cost

pr_mean = 35 # Mean of dispose cost
pr_range = 1 # Range of dispose cost

hn_mean = 28 # Mean of holding cost of manufacturing products
hn_range = 2 # Range of holding cost of manufacturing products

hs_mean = 20 # Mean of holding cost of remanufacturing products
hs_range = 1 # Range of holding cost of remanufacturing products

hr_mean = 11 # Mean of holding cost of returns
hr_range = 1 # Range of holding cost of returns

##### Code

def parse_args():
    """ Parse flags and store arguments in the global variable `args`."""
    global args
    parser = argparse.ArgumentParser(description='Generate a .dat file following type of the chosen lot sizing problem. All the values are integers.')
    parser.add_argument("-c", "--capacitated", action="store_true", help="The lot sizing problem include capacity")
    parser.add_argument("-C", action="store_true", help="The capacity of new and remanufactured products is common")
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


def adjust_returns():
    """Adjusts the Returns list so that there exists a solution to the lot sizing problem
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


def adjust_capacitated_uncommon():
    """ Adjusts lists of returns and demands so that there exists a solution to the lot sizing
    problem with uncommon capacity.
    Returns a boolean indication whether a change has been made or not."""
    M_t = 0
    M_t1 = 0
    R_1_t = 0
    Ds_1_t = 0
    Dn_1_t = 0
    modified = False
    for t in range(args.T):
        Ds_1_t += Ds[t]
        Dn_1_t += Dn[t]
        R_1_t += R[t]
        M_t1 = M_t + min(R_1_t - M_t, Cs)
        while M_t1 < Ds_1_t:
            modified = True

            if R_1_t - M_t < Cs:
                # If the problem is maybe the lack of returns
                R_1_t -= R[t]
                R[t] = min(Cs, Ds[t])
                R_1_t += R[t]
            else:
                # If the problem is the demand that is too high
                Ds_1_t -= Ds[t]
                Ds[t] = min(max(1, R[t] + rd.randint(0, R_range)), Cs)
                Ds_1_t += Ds[t]

            M_t1 = M_t + min(R_1_t - M_t, Cs)
        M_t = M_t1

        while (t + 1) * Cn  < Dn_1_t:
            modified = True

            temp = Dn_1_t
            Dn_1_t -= Dn[t]
            Dn[t] = max(1, Cn - rd.randint(-Dn_range, Dn_range))
            Dn_1_t += Dn[t] 
    
    return modified


def verifiy_constraints():
    """ Verify that constraints on costs are verified """

    # Constraint non-speculative costs of new products (2.1.n)
    if not(hn_mean - hn_range > 2 * pn_range):
        print("New products costs are not strictly non-speculative.")
    
    # Constraint non-speculative costs of remanufactured products (2.1.s)
    if not(hs_mean - hs_range > 2 * ps_range):
        print("Remanufactured products costs are not strictly non-speculative.")
    
    # Constraint non-speculative costs of returns (2.1.r)
    if args.dispose and not(hr_mean - hr_range > 2 * pr_range):
        print("Returns costs are not strictly non-speculative.")

    # Constraint return-advantage costs (2.2)
    if not(hs_mean - hs_range > hr_mean + hr_range + 2 * ps_range):
        print("Return-advantage costs are not verified.")
    
    # Constraint of possible null demand:
    if Ds_mean - Ds_range <= 0 or Dn_mean - Dn_range <= 0:
        print("Demand values can be null.")


def generate_example():
    """ Create the .dat file with the constraints set by the problem."""
    global Dn, Ds, R, f, pn, ps, pr, hn, hs, hr

    # Demand
    Dn = create_random_list(Dn_mean, Dn_range)
    Ds = create_random_list(Ds_mean, Ds_range)

    # Returns
    if args.returns:
        R = create_random_list(R_mean, R_range)

    # Setup costs
    f = create_random_list(f_mean, f_range)

    # Production costs
    pn = create_random_list(pn_mean, pn_range)
    ps = create_random_list(ps_mean, ps_range)

    # Dispose
    if args.dispose:
        pr = create_random_list(pr_mean, pr_range)
    
    # Storage costs
    hn = create_random_list(hn_mean, hn_range)
    hs = create_random_list(hs_mean, hs_range)
    hr = create_random_list(hr_mean, hr_range)


def verify_feasibility():
    """ Verify feasibility of the generated instance and adjusts data if not """

    if args.capacitated and adjust_capacitated_uncommon():
        print("The list of returns and demand has been adjusted for a solution to exist.")
    
    elif adjust_returns():
        print("The list of returns has been adjusted for a solution to exist.")

    


def write_example():
    """ Write the example in the file."""

    file = open(args.file, "w")

    # Length of the horizon
    file.write(f"T = {args.T};\n")

    # Demand
    file.write(f"Dn = {Dn};\n")
    file.write(f"Ds = {Ds};\n")

    # Returns
    if args.returns:
        file.write(f"R = {R};\n")
    
    # Setup costs
    file.write(f"f = {f};\n")

    # Production costs
    file.write(f"pn = {pn};\n")
    file.write(f"ps = {ps};\n")

    # Dispose
    if args.dispose:
        file.write(f"pr = {pr};\n")

    # Storage costs
    file.write(f"hn = {hn};\n")
    file.write(f"hs = {hs};\n")
    file.write(f"hr = {hr};\n")

    # Production capacity
    if args.capacitated:
        if args.C:
            file.write(f"C = {C};\n")
        else:
            file.write(f"Cs = {Cs};\n")
            file.write(f"Cn = {Cn};\n")
    
    file.close()


def main():
    """ Main fonction. Only executed when the script is runned (not imported)."""
    parse_args()
    
    verifiy_constraints()

    generate_example()

    verify_feasibility()

    write_example()

    return 1


if __name__=="__main__":
    main()