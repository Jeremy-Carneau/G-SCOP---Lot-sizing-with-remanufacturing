
// Uncapacitated with dispose lot sizing problem

/*
    Data
*/

int T = ... ; // Length of the horizon
range periods = 1..T ;

float Dn[periods] = ... ; // Demand of manufactured products
float Ds[periods] = ... ; // Demand of remanufactured products

float R[periods] = ... ; // Returns (at the beginning of the period)

float f[periods] = ... ; // Fixed joint setup cost

float pn[periods] = ... ; // Variable manufacturing cost
float ps[periods] = ... ; // Variable remanufacturing cost
float pr[periods] = ... ; // Variable cost to dispose returns

float hn[periods] = ... ; // Holding cost of manufactured products
float hs[periods] = ... ; // Holding cost of remanufactured products
float hr[periods] = ... ; // Holding cost of returns

float M = sum (t in periods) (Dn[t] + Ds[t]); // Max of production
// TODO : reduce M value to be more efficient

/*
    Variables declaration
*/

dvar float+ xn[periods]; // Number of manufactured products
dvar float+ xs[periods]; // Number of remanufactured products
dvar float+ xr[periods]; // Number of disposed return products

dvar float+ sn[0..T]; // Inventory of manufactured products
dvar float+ ss[0..T]; // Inventory of remanufactured products
dvar float+ sr[0..T]; // Inventory of returns

dvar boolean y[periods]; // y[t] = 1 if production is launched at period t, else 0

/*
    Objective fonction
*/

minimize sum (t in periods) ((pn[t] * xn[t] + ps[t] * xs[t]) // Variable costs
                            + (hn[t] * sn[t] + hs[t] * ss[t] +  hr[t] * sr[t]) // Holding costs
                            + f[t] * y[t] // Setup cost
                            + pr[t] * xr[t]); // Dispose cost

/*
    Constraints
*/

subject to {

    // Stock is empty at first
    sn[0] == 0;
    ss[0] == 0;
    sr[0] == 0;
    ss[T] == 0;
    sn[T] == 0;
    sr[T] == 0;
    
    // We respond to demand
    forall (t in periods) xn[t] + sn[t - 1] == sn[t] + Dn[t];
    forall (t in periods) xs[t] + ss[t - 1] == ss[t] + Ds[t];

    // Returns management
    forall (t in periods) R[t] + sr[t - 1] == xr[t] + sr[t] + xs[t];

    // In order to include production cost
    forall (t in periods) xn[t] + xs[t] <= M * y[t];
}

/* Display */
execute {
    writeln("Post-traitement: ");
    writeln("La valeur de l'objectif est de "+cplex.getObjValue());
    writeln("Données :")
    writeln("Dn = ", Dn);
    writeln("Ds = ", Ds);

    writeln("T = ", T);
    writeln("R = ", R);

    writeln("xn = ", xn);
    writeln("xs = ", xs);
    writeln("xr = ", xr);

    writeln("sn = ", sn);
    writeln("ss = ", ss);
    writeln("sr = ", sr);
} 