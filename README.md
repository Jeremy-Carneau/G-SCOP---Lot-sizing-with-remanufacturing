# Objectives

We need to begin to analyze the uncapacitated lot sizing problem with and without dispose cases first (dispose = we can discard/sell stock of return ; treat both cases when this discard is a profit or a loss).


When finished, we can start including capacity (start without dispose first).


Take care of including holding costs increasing with the quality of the products ($h_t^r <= h_t^s <= h_t^n$).

# To do list

## Programming section

- [x] Automate generation of flow graphs from linear program (LP) resolution (see if it is possible with Python or something, otherwise use LateX with tikz)

## Test section

- [x] Generate different tests (variation of costs, ...) with at least 30 periods

## Mathematical section

- [x] Find solution properties about the problem with and without dispose

### Without dispose

- [ ] Prove that there exists an optimal solution that respects Wagner-Within property for new products

- [ ] Prove that there exists an optimal solution that respects Wagner-Within property for remanufacturial products

- [ ] Prove that there exists an optimal solution when new products and remanufacturial products are products at the same periods
### With dispose

- [ ] Prove that there exists an optimal solution that respects Wagner-Within property for new products

- [ ] Prove that there exists an optimal solution that respects Wagner-Within property for remanufacturial products

- [ ] Prove that there exists an optimal solution when new products and remanufacturial products are products at the same periods

- [ ] Define a subplan structure (4 indexes)

- [ ] Prove that there exists an optimal solution when we dispose at the beginning of each subplan

- [ ] Prove that each subplan are independant (the sum of optimal solution of each subplan is an optimal solution of the global problem)
# Notes

All the Python scripts (my_program.py) have user guide running <code>my_program.py -h</code> or <code>my_program.py --help</code>.
# Notations

## Parameters

Parameters in each period $t$ ($T$ the length of the horizon):
- $D^n_t$: Demand of manufactured products (new) (satisfied at the end of the period);
- $D^s_t$: Demand of remanufactured products (second-hand) (satisfied at the end of the period);
- $R_t$: Returns (at the beginning of the period);
- $f_t$: Fixed joint setup cost;
- $p^s_t$: Variable remanufacturing cost;
- $p^n_t$: Variable manufacturing cost;
- $p^r_t$: Variable cost to dispose returns;
- $h^s_t$: Holding cost of remanufactured products;
- $h^n_t$: Holding cost of manufactured products;
- $h^r_t$: Holding cost of returns;
- $C^s_t$: Remanufacturing capacity;
- $C^n_t$: Manufacturing capacity;
- $C_t$: Manufacturing and remanufacturing capacity (In case of common capacity);

## Decision variables

Decision variables in each period $t$:

- $x^s_t$: Number of remanufactured products;
- $x^n_t$: Number of manufactured products;
- $x^r_t$: Number of disposed return products;
- $y_t$: 1 if $x^s_t + x^n_t > 0$, 0 otherwise;
- $s^s_t$: Inventory of remanufactured products (at the end of the period);
- $s^n_t$: Inventory of manufactured products (at the end of the period);
- $s^r_t$: Inventory of returns (at the end of the period);