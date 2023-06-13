
/*
    Data
*/

int T = ... ; // Number of periods
range periods = 1..T ;

float dn[periods] = ... ; // Demand of new products
float dr[periods] = ... ; // Demand of remanufactured products

float f[periods] = ... ; // Launching production costs

float pn[periods] = ... ; // Unit production costs of new products
float pr[periods] = ... ; // Unit production costs of remanufactured products

float hn[periods] = ... ; // Unit storage costs of new products
float hr[periods] = ... ; // Unit storage costs of remanufactured products

float C[periods] = ... ; // Production capacities

float M = sum (t in periods) (dn[t] + dr[t]); // Max of production

/*
    Variables declaration
*/

dvar float+ xn[periods]; // number of new products created at period t
dvar float+ xr[periods]; // number of remanufactured products created at period t

dvar float+ sn[0..T]; // number of new products in stock at period t
dvar float+ sr[0..T]; // number of remanufactured in stock at period t

dvar boolean y[periods]; // y[t] = 1 if production is launched at period t, else 0

/*
    Objective fonction
*/

minimize sum (t in periods) ((pn[t] * xn[t] + pr[t] + xr[t]) + (hn[t] * sn[t] + hr[t] * sr[t]) + f[t] * y[t]);
// + hR ...

/*
    Constraints
*/

subject to {

    // For each period, we only produce or we only store
    // forall (t in periods) sn[t - 1] <= M * (1 - y[t]);
    // forall (t in periods) sr[t - 1] <= M * (1 - y[t]);

    // Stock is empty at first and at the end
    sn[0] == 0;
    sr[0] == 0;
    // sn[T] == 0;
    // sr[T] == 0;
    
    // We respond to demand
    forall (t in periods) xn[t] + sn[t - 1] - sn[t] == dn[t];
    forall (t in periods) xr[t] + sr[t - 1] - sr[t] == dr[t];
    
    // If we produce then we must respect production capacities
    forall (t in periods) xn[t] + xr[t] <= C[t] * y[t];
}

/* Display */
execute {
    writeln("Post-traitement: ");
    writeln("La valeur de l'objectif est de "+cplex.getObjValue());

    writeln("");
    writeln("Valeurs de production: ");
    writeln("Produits neufs:          ", xn);
    writeln("Produits remanufacturés: ", xr);

    writeln("");
    writeln("Valeurs de stockage: ");
    writeln("Stocks neufs:            ", sn);
    writeln("Stocks remanufacturés:   ", sr);
} 