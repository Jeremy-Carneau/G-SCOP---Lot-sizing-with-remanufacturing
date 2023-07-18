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

## Collect date from OPL results

def read_line(line):
    res = []
    res.append(float(line[2][1:]))
    for x in line[3:-1]:
        res.append(float(x))
    res.append(float(line[-1][:-1]))
    return res


def collect_data(filename):
    """ Read the result from an OPL script and put the results
    in global variables """
    global T, xn, xs, xr, R, sn, ss, sr

    T = None
    xr = []
    sr = []
    R = []

    file = open(filename, 'r')

    for lines in file:
        current = lines.split()
        if len(current) == 0:
            continue
        # Only read data
        if current[0] not in {"T", "xn", "xs", "xr", "sn", "ss", "sr", "R"}:
            continue

        if current[0] == "T":
            line = current
        else:
            line = ""
            temp_line = lines
            if len(temp_line) != 0:
                # We test if the list is writen on several lines
                test = temp_line.split()[-1][-1]
                while test != "]":
                    line += temp_line
                    temp_line = file.readline()
                    if len(temp_line) == 0:
                        break
                    test = temp_line.split()[-1][-1]
                line += temp_line
            
            line = line.split()

            
        match line[0]:
            case "T":
                T = int(line[2])
            case "xn":
                xn = read_line(line)
            case "xs":
                xs = read_line(line)
            case "xr":
                xr = read_line(line)
            case "sn":
                sn = read_line(line)
            case "ss":
                ss = read_line(line)
            case "sr":
                sr = read_line(line)
            case "R":
                R = read_line(line)
            case other:
                continue

    file.close()

    # Data verifications
    if T is None:
        print("The problem has no solution")
        exit(1)
    
    assert(len(xn) == T)
    assert(len(xs) == T)
    assert(len(sn) == T + 1)
    assert(len(ss) == T + 1)


    if len(xr) > 0:
        assert(len(xr) == T) 
    else:
        xr = [0] * T
    
    if len(sr) > 0:
        assert(len(sr) == T + 1)
    else:
        sr = [0] * (T + 1)
    
    if len(R) > 0:
        assert(len(R) == T)
    else:
        R = [0] * T


## Graph creation

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

    # Nodes for remanufactured product demand
    for j in range(T):
        node_label = f"Ds[{j}]"
        G.add_node(node_label, pos=(j + 0.3, 2.2), color='white', label_visible = False)

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
        G.add_node(node_label, pos=(j + 0.3, 0), color='white', label_visible = False)

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
        if E < xn[i] - sn[i + 1] + sn[i]:
            G.add_edge(f"N[{i}]", f"Dn[{i}]", color='black', weight=xn[i] - sn[i + 1] + sn[i])

        if E < xs[i] - ss[i + 1] + ss[i]:
            G.add_edge(f"S[{i}]", f"Ds[{i}]", color='black', weight=xs[i] - ss[i + 1] + ss[i])

        # Dispose
        if E < xr[i]:
            G.add_edge(f"R[{i}]", f"D[{i}]", color='black', weight=xr[i])

        # Returns
        if E < R[i]:
            G.add_edge(f"RR[{i}]", f"R[{i}]", color='blue', weight=R[i])

        # Remanufactured production
        if E < xs[i]:
            G.add_edge(f"R[{i}]", f"S[{i}]", color='blue', weight=xs[i])


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
    mng = plt.get_current_fig_manager() 
    mng.resize(*mng.window.maxsize())
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

    plt.switch_backend('TkAgg')

    collect_data(filename)

    generate_graph()

    return 1

if __name__=="__main__":
    main()