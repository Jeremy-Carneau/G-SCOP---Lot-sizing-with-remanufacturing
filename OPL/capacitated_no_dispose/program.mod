
// Uncapacitated with dispose lot sizing problem

/*
    Data
*/

int T = ... ; // Length of the horizon
range periods = 1..T ;

int Dn[periods] = ... ; // Demand of manufactured products
int Ds[periods] = ... ; // Demand of remanufactured products

int R[periods] = ... ; // Returns (at the beginning of the period)

int f[periods] = ... ; // Fixed joint setup cost

int pn[periods] = ... ; // Variable manufacturing cost
int ps[periods] = ... ; // Variable remanufacturing cost

int hn[periods] = ... ; // Holding cost of manufactured products
int hs[periods] = ... ; // Holding cost of remanufactured products
int hr[periods] = ... ; // Holding cost of returns

int Cs = ...; // Production capacity of remanufactured products 
int Cn = ...; // Production capacity of new products 


/*
    Variables declaration
*/

dvar int+ xn[periods]; // Number of manufactured products
dvar int+ xs[periods]; // Number of remanufactured products

dvar int+ sn[0..T]; // Inventory of manufactured products
dvar int+ ss[0..T]; // Inventory of remanufactured products
dvar int+ sr[0..T]; // Inventory of returns

dvar boolean y[periods]; // y[t] = 1 if production is launched at period t, else 0

/*
    Objective fonction
*/

minimize sum (t in periods) ((pn[t] * xn[t] + ps[t] * xs[t]) // Variable costs
                            + (hn[t] * sn[t] + hs[t] * ss[t] +  hr[t] * sr[t]) // Holding costs
                            + f[t] * y[t]); // Setup cost

/*
    Constraints
*/

subject to {

    // Stock is empty at first
    sn[0] == 0;
    ss[0] == 0;
    sr[0] == 0;
    
    // We respond to demand
    forall (t in periods) xn[t] + sn[t - 1] == sn[t] + Dn[t];
    forall (t in periods) xs[t] + ss[t - 1] == ss[t] + Ds[t];

    // Returns management
    forall (t in periods) R[t] + sr[t - 1] == sr[t] + xs[t];

    // Capacity constraints
    forall (t in periods) xs[t] <= Cs * y[t];
    forall (t in periods) xn[t] <= Cn * y[t];
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

    writeln("sn = ", sn);
    writeln("ss = ", ss);
    writeln("sr = ", sr);
} 