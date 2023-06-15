#!/usr/bin/python3

"""
Plot the flow graph of the OPL results put in the file in argument.
"""

##### Imports

import networkx as nx
import matplotlib.pyplot as plt
import sys

##### Global variables

E = 0.001 # Under this value, the flow is considered equals to 0

##### Code

# Création du graphe

def collect_data(filename):
    """ Read the result from an OPL script and put the results
    in global variables """
    global T, xn, xs, xr, R, sn, ss, sr

    T = 6
    xn = [20, 12, 16, 30, 0, 19]
    xs = [9, 9, 14, 0, 12, 13]
    xr = [4, 11, 1, 17, 0, 0]

    R = [13, 20, 15, 19, 10, 16]

    sn = [0, 0, 0, 0, 11, 0, 0]
    ss = [0, 0, 0, 6, 0, 0, 0]
    sr = [0, 0, 0, 0, 2, 0, 3]


def generate_graph():
    """ Plot the flow graph related to global variables generated 
    from `collect_data` """

    G = nx.DiGraph()

    # Return imports nodes
    for j in range(T):
        node_label = f"RR[{j}]"
        G.add_node(node_label, pos=(j - 0.25, 5), color='white', label_visible = False)

    # Dispose nodes
    for j in range(T):
        node_label = f"D[{j}]"
        G.add_node(node_label, pos=(j + 0.25, 5), color='white', label_visible = False)


    # Returns nodes
    for j in range(T):
        node_label = f"R[{j}]"
        G.add_node(node_label, pos=(j, 4), color='lightblue', label_visible = True)
    node_label = f"R[{T}]"
    G.add_node(node_label, pos=(T, 4), color='red', label_visible = False)

    # Remanufactured products nodes
    for j in range(T):
        node_label = f"S[{j}]"
        G.add_node(node_label, pos=(j, 3), color='lightgreen', label_visible = True)
    node_label = f"S[{T}]"
    G.add_node(node_label, pos=(T, 3), color='red', label_visible = False)

    # Nodes for new product demand
    for j in range(T):
        node_label = f"Ds[{j}]"
        G.add_node(node_label, pos=(j, 2.2), color='white', label_visible = False)

    # Production nodes for new products
    for j in range(T):
        node_label = f"xn[{j}]"
        G.add_node(node_label, pos=(j, 1.8), color='white', label_visible = False)


    # New products nodes
    for j in range(T):
        node_label = f"N[{j}]"
        G.add_node(node_label, pos=(j, 1), color='lightyellow', label_visible = True)
    node_label = f"N[{T}]"
    G.add_node(node_label, pos=(T, 1), color='red', label_visible = False)

    # Nodes for new product demand
    for j in range(T):
        node_label = f"Dn[{j}]"
        G.add_node(node_label, pos=(j, 0), color='white', label_visible = False)

    ## Edge generation

    for i in range(T):
        # Stocks
        if E < sn[i + 1]:
            G.add_edge(f"N[{i}]", f"N[{i + 1}]", color="green", weight=sn[i+1])

        if E < sr[i + 1]:
            G.add_edge(f"R[{i}]", f"R[{i + 1}]", color='green', weight=sr[i+1])

        if E < ss[i + 1]:
            G.add_edge(f"S[{i}]", f"S[{i + 1}]", color='green', weight=ss[i+1])

        # Production of new products
        if E < xn[i]:
            G.add_edge(f"xn[{i}]", f"N[{i}]", color='red', weight=xn[i])

        # Demand
        if E < xn[i] - sn[i + 1]:
            G.add_edge(f"N[{i}]", f"Dn[{i}]", color='black', weight=xn[i] - sn[i + 1])

        if E < xs[i] - ss[i + 1]:
            G.add_edge(f"S[{i}]", f"Ds[{i}]", color='black', weight=xs[i] - ss[i + 1])

        # Dispose
        if E < xr[i]:
            G.add_edge(f"R[{i}]", f"D[{i}]", color='black', weight=xr[i])

        # Returns
        if E < R[i]:
            G.add_edge(f"RR[{i}]", f"R[{i}]", color='blue', weight=R[i])

        # Remanufactured production
        p = xs[i] - ss[i]
        if E < p:
            G.add_edge(f"R[{i}]", f"S[{i}]", color='blue', weight=p)


    edge_colors = [G.edges[edge]['color'] for edge in G.edges]
    node_colors = [G.nodes[node]['color'] for node in G.nodes]
    labels = {node: node for node in G.nodes if G.nodes[node].get('label_visible', True)}
    pos = nx.get_node_attributes(G, 'pos')

    nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_size=1000, 
            edge_color=edge_colors, node_color=node_colors, font_size=10,
            arrows=True, font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Lot sizing flow graph")
    plt.axis('equal')
    plt.show()

def main():
    if len(sys.argv) < 2:
        filename = "res.txt"
    else:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("""usage : graph_generation [(optionnal : default=`res.txt`) FILENAME]
                  \nPlot the flow graph of the OPL results put in the file in argument.""")
            exit(0)
        filename = sys.argv[1]

    collect_data(filename)

    generate_graph()

    return 1

if __name__=="__main__":
    main()