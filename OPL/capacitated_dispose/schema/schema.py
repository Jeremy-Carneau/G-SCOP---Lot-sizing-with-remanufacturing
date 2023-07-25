#!/usr/bin/python3

"""
Just a file to print graphs for the report
"""

##### Imports

import networkx as nx
import matplotlib.pyplot as plt
import sys

##### Global variables

T = 15
stock_color="blue"
prod_color = "green"
dl = 5
dr = 13
pl = 8
pr = 11
pn = 15
Xl = 2
Xr = 2


##### Code

def plot_graph():
    """ Generate the example and plot it """

    plt.switch_backend('TkAgg')
    G = nx.DiGraph()

    ### Labels
    G.add_node("Returns stock", pos=(0, 4), color='white', label_visible = True)
    G.add_node("Remanufacturing", pos=(0, 3), color='white', label_visible = True)
    G.add_node("New products", pos=(0, 1), color='white', label_visible = True)

    ### Nodes
    for j in range(1, T + 1):
        G.add_node(f"label{j}", pos =(j, 5.5),color='white', label_visible = False)
        G.add_node(f"R{j}", pos=(j, 4), color='lightblue', label_visible = False)
        G.add_node(f"S{j}", pos=(j, 3), color='lightgreen', label_visible = False)
        G.add_node(f"N{j}", pos=(j, 1), color='yellow', label_visible = False)

        G.add_node(f"RR{j}", pos=(j-0.3, 4.8), color='white', label_visible = False)
        G.add_node(f"D{j}", pos=(j+0.3, 4.8), color='white', label_visible = False)
        G.add_node(f"Ds{j}", pos=(j+0.3, 2.2), color='white', label_visible = False)
        G.add_node(f"xn{j}", pos=(j, 2.0), color='white', label_visible = False)
        G.add_node(f"Dn{j}", pos=(j+0.3, 0.2), color='white', label_visible = False)
    G.add_node(f"R{T + 1}", pos=(T + 1, 4), color='white', label_visible = False)

    ### Edges
    for i in range(1, T + 1):
        G.add_edge(f"RR{i}", f"R{i}", color='black', weight=-1)
        G.add_edge(f"S{i}", f"Ds{i}", color="black", weight=-1)
        G.add_edge(f"N{i}", f"Dn{i}", color="black", weight=-1)

    # Production
    for i in {1, 2, 4, 6, 7, 8, 9, 11, 12, 13, 15}:
        w = "C" if i in {4, 6, 7, 9, 12, 13} else -1
        G.add_edge(f"R{i}", f"S{i}", color=prod_color, weight=w)

        w = "C" if i in {4, 6, 8, 9, 12, 13} else -1
        G.add_edge(f"xn{i}", f"N{i}", color=prod_color, weight=w)

    # Returns stock
    for i in range(1, T):
        if i not in {4, 12}:
            G.add_edge(f"R{i}", f"R{i + 1}", color=stock_color, weight=-1)
    G.add_edge(f"R{T}", f"R{T + 1}", color=stock_color, weight=-1)

    # Remanufactured stock
    for i in {2, 3, 4, 5, 6, 8, 9, 11, 12, 13}:
        G.add_edge(f"S{i}", f"S{i + 1}", color=stock_color, weight=-1)
    
    # New stock
    for i in {2, 3, 4, 5, 7, 8, 9, 11, 12, 13}:
        G.add_edge(f"N{i}", f"N{i + 1}", color=stock_color, weight=-1)
    
    # Dispose
    for i in {1, 5, 13}:
        G.add_edge(f"R{i}", f"D{i}", color=stock_color, weight=-1)

    ### Graph drawing
    edge_colors = [G.edges[edge]['color'] for edge in G.edges]
    node_colors = [G.nodes[node]['color'] for node in G.nodes]
    labels = {node: node for node in G.nodes if G.nodes[node].get('label_visible', True)}
    labels.update({f"label{dl}" : "dl", f"label{dr}" : "dr", f"label{pl}" : "pl", f"label{pr}" : "pr",
                   f"label{pn}" : "pn"})
    pos = nx.get_node_attributes(G, 'pos')

    nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_size=1000, 
            edge_color=edge_colors, node_color=node_colors, font_size=10,
            arrows=True, font_weight='bold')

    edge_labels = {edge: weight for edge, weight in nx.get_edge_attributes(G, 'weight').items() if weight != -1 }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, rotate=False)

    dashed_edges = [(f"label{dl}", f"R{dl}"),(f"label{dr}", f"R{dr}"),(f"label{pl}", f"R{pl}"),
                    (f"label{pr}", f"R{pr}"),(f"label{pn}", f"R{pn}")]
    nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, style='dashed')

    mng = plt.get_current_fig_manager() 
    mng.resize(*mng.window.maxsize())
    plt.axis('equal')
    plt.show()


def main():
    if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("""usage : schema [-h]
              \nPlot the graph of an example for illustrating the report.""")
        exit(0)

    plot_graph()

    return 1

if __name__=="__main__":
    main()

