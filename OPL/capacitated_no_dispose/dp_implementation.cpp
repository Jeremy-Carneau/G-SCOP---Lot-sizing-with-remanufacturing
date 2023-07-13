#include <iostream>
#include <vector>
#include <cmath>

#define ll long long
#define INF -1
#define MIN(u,v) (u==-1?v:(v==-1?u:min(u,v))) 
#define CEIL(x,y) (x/y + (x%y?1:0))  //returns ceil(x/y)

using namespace std;


char ignore_char;

int T;         // Number of periods
vector<ll> Dn; // Manufactured demand
vector<ll> Ds; // Remanufactured demand
vector<ll> R;  // Number of returns
vector<ll> f;  // Setup cost
vector<ll> pn; // Manufacturing cost
vector<ll> ps; // Remanufacturing cost
vector<ll> hn; // Holding cost of manufactured products 
vector<ll> hs; // Holding cost of remanufactured products
vector<ll> hr; // Holding cost of returns
ll Cs;         // Production capacity of remanufactured products
ll Cn;         // Production capacity of manufactured products

vector<vector<ll>> Dn_rng; // contains the range sum of Dn for all ranges [i,j] where j>=i
vector<vector<ll>> Ds_rng; // contains the range sum of Ds for all ranges [i,j] where j>=i
vector<vector<ll>> R_rng;  // contains the range sum of R  for all ranges [i,j] where j>=i

vector<vector<vector<vector<vector<ll>>>>> dp; // the dp vector

void ignore_chars(int number_of_chars){
    for(int i = 0; i < number_of_chars; i++){
        cin>>ignore_char;
    }
}

void read_vector(vector<ll> &vec, string name_of_vec){
    //set vector size to T+1
    vec.resize(T+1);

    int len_name = name_of_vec.length();
    //ignore the "{vector_name} = ["
    ignore_chars(len_name+2);
    //read the vector
    for(int i = 0; i < T; i++){
        //get the i-th value of the vector
        cin>>vec[i];
        //ignore the ", " or the "];" at the end
        ignore_chars((i<T-1 ? 1 : 2));
    }
}

template <typename N>
void read_value(N &var, string var_name){
    int len_name = var_name.length();
    //ignore the "{var_name} = "
    ignore_chars(len_name+1);
    //read the variable
    cin>>var;
    //ignore the ;
    ignore_chars(1);
}

void parse_params(){
    //get T
    read_value(T, "T");

    //get Dn
    read_vector(Dn, "Dn");
    //get Ds
    read_vector(Ds, "Ds");
    //get R
    read_vector(R, "R");
    //get f
    read_vector(f, "f");
    //get pn
    read_vector(pn, "pn");
    //get ps
    read_vector(ps, "ps");
    //get hn
    read_vector(hn, "hn");
    //get hs
    read_vector(hs, "hs");
    //get hr
    read_vector(hr, "hr");

    //get Cs
    read_value(Cs, "Cs");
    //get Cn
    read_value(Cn, "Cn");
}

void calc_range_sum(vector<ll> &vec, vector<vector<ll>> &vec_range_sum){
    int n = vec.size();
    vec_range_sum.resize(n, vector<ll>(n));
    for(int i=0;i<n;i++){
        vec_range_sum[i][i] = vec[i];
        for(int j=i+1; j<n; j++){
            vec_range_sum[i][j] = vec_range_sum[i][j-1] + vec[j];
        }
    }
}


int main(){
    //input parsing
    parse_params();

    //calculating all the needed range sums
    calc_range_sum(Dn, Dn_rng);
    calc_range_sum(Ds, Ds_rng);
    calc_range_sum(R, R_rng);

    //executing the main dp algorithm

    dp.resize(T+1, vector<vector<vector<vector<ll>>>>(T+1,
                    vector<vector<vector<ll>>>(T+1,
                    vector<vector<ll>>(T+1,
                    vector<ll>(T+1, INF)))));


    //base case
    dp[T][T][T][0][0] = 0;
    for(int t = T-1; t>=0; t--){
        for(int ks = T; ks >= t; ks--){
            for(int kn = T; kn >= t; kn--){
                for(int Ns = ks - t; Ns >=0; Ns--){
                    for(int Nn = kn - t; Nn>=0; Nn--){
                        if(t==ks && t==kn){
                            if(Ns>0 || Nn>0) continue;
                            for(int i=t; i<T; i++)
                                for(int j=t; j<T; j++)
                                    dp[t][t][t][0][0] = MIN(dp[t][t][t][0][0], dp[t][i+1][j+1][CEIL(Ds_rng[t][i], Cs)][CEIL(Dn_rng[t][j], Cn)]);
                        }
                        else if(t==ks){
                            if(Ns>0) continue;
                            for(int i=t; i<T; i++)
                                dp[t][t][kn][0][Nn] = MIN(dp[t][t][kn][0][Nn], dp[t][i+1][kn][CEIL(Ds_rng[t][i], Cs)][Nn]);
                        }
                        else if(t==kn){
                            if(Nn>0) continue;
                            for(int j=t; j<T; j++)
                                dp[t][ks][t][Ns][0] = MIN(dp[t][ks][t][Ns][0], dp[t][ks][j+1][Ns][CEIL(Dn_rng[t][j], Cn)]);
                        }
                        else{
                            //cost in case of production
                            ll production_case_cost = 0;

                            //storage for s
                            ll Ss = (t==ks-1 ? 0 : Ds_rng[t+1][ks-1]-(Ns-1)*Cs); 
                            if(Ss<0) production_case_cost = INF;
                            //storage for r
                            ll Sr = (R_rng[0][t] - Ds_rng[0][t]) - Ss;
                            if(Sr<0) production_case_cost = INF;
                            //storage for n
                            ll Sn = (t==kn-1 ? 0 : Dn_rng[t+1][kn-1]-(Nn-1)*Cn); 
                            if(Sn<0) production_case_cost = INF;
                            //production for s
                            ll Xs = (Ds_rng[t][ks-1]<=Ns*Cs ? Ds_rng[t][ks-1] - (Ns-1)*Cs : Cs);
                            if(Xs<=0) production_case_cost = INF;
                            //production for n
                            ll Xn = (Dn_rng[t][kn-1]<=Nn*Cn ? Dn_rng[t][kn-1] - (Nn-1)*Cn : Cn);
                            if(Xn<=0) production_case_cost = INF;

                            if(production_case_cost!=INF && Ns>0 && Nn>0 && dp[t+1][ks][kn][Ns-1][Nn-1]!=INF){
                                production_case_cost = dp[t+1][ks][kn][Ns-1][Nn-1] + hs[t]*Ss + hr[t]*Sr + hn[t]*Sn + ps[t]*Xs + pn[t]*Xn + f[t];
                            }
                            else production_case_cost = INF;

                            //cost in case of no production
                            ll no_production_case_cost = 0;

                            //storage for s
                            Ss = (t==ks-1 ? 0 : Ds_rng[t+1][ks-1]-Ns*Cs); 
                            if(Ss<0) no_production_case_cost = INF;
                            //storage for r
                            Sr = (R_rng[0][t] - Ds_rng[0][t]) - Ss;
                            if(Sr<0) no_production_case_cost = INF;
                            //storage for n
                            Sn = (t==kn-1 ? 0 : Dn_rng[t+1][kn-1]-Nn*Cn); 
                            if(Sn<0) no_production_case_cost = INF;

                            if(no_production_case_cost!=INF && dp[t+1][ks][kn][Ns][Nn]!=INF){
                                no_production_case_cost = dp[t+1][ks][kn][Ns][Nn] + hs[t]*Ss + hr[t]*Sr + hn[t]*Sn;
                            }
                            else no_production_case_cost = INF;

                            //min between the two cases
                            dp[t][ks][kn][Ns][Nn] = MIN(production_case_cost, no_production_case_cost);
                        }
                    }
                }
            }
        }
    }
    cout<<dp[0][0][0][0][0]<<endl;

}