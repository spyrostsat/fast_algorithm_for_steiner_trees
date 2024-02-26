from src.utils import *
from src.interfaces import *
import networkx as nx
import random


START = 6
END = 13
EDGES_INCREASE = 3

for i in range(START, END):
    G = nx.gnm_random_graph(n=i, m=i+EDGES_INCREASE)
    
    for u, v in G.edges:
        G[u][v]["weight"] = random.randint(1, 50)
    
    G:nx.Graph = nx.relabel_nodes(G, {node: f"V{node+1}" for node in range(i)})  # vertices will be named from "V1" to "Vn"
    S:IVertices = random.sample(list(G.nodes), round(0.7*i))  # randomly select 70% of the vertices to be the Steiner vertices
    
    try:
        Ts = solve_steiner_tree_problem(G=G, S=S, plot_charts=True)
        print(f"Nodes: {i} | Total weight of Steiner Tree: {calculate_total_weight_of_graph(Ts)}")
    except nx.exception.NetworkXNoPath:
        print(f"Nodes: {i} | No available Steiner Tree. The graph is not connected.")
